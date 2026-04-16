from __future__ import annotations


from pathlib import Path

from ..utils.logging_utils import Logger
import json

from ..utils.common_utils import convert_to_json_serializable, InlineJSONEncoder, wrap_leaf_lists_as_rawjson, get_clean_filename, get_optimized_filename
from ..utils.conservation_utils import load_msa_sto,load_msa_aligned_fasta,load_msa_a3m, write_sto,write_aligned_fasta,write_a3m
from typing import List, Dict,Any, Tuple
import subprocess




def file_exists(path: str | Path) -> bool:
    p = Path(path)
    return p.exists() and p.is_file()

def get_stem(input_path: str | Path) -> str:
    return Path(input_path).stem

MAXFILENAME=150

def check_filename_length(name: str, logger: Logger) -> bool:
    if len(name) > MAXFILENAME:
        logger.print(f"[ERROR] Filename too long (>{MAXFILENAME}): {name}")
        return False
    return True


def write_json_from_dict_inline_leaf_lists(dict_data: dict, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dict_data = convert_to_json_serializable(dict_data)
    dict_data = wrap_leaf_lists_as_rawjson(dict_data)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            dict_data,
            f,
            cls=InlineJSONEncoder,
            indent=2,
            ensure_ascii=False
        )


def load_msa(path: str | Path, logger: Logger) -> List[Dict[str, str]] | None:
    p = Path(path)

    try:
        suffix = p.suffix.lower()

        if suffix in {".sto", ".stockholm"}:
            return load_msa_sto(p, logger)

        elif suffix in {".fa", ".fasta", ".afa"}:
            return load_msa_aligned_fasta(p, logger)

        elif suffix == ".a3m":
            return load_msa_a3m(p, logger)

        else:
            logger.print(f"[ERROR] Unsupported MSA format: {str(p)}")
            return None

    except Exception as e:
        logger.print(f"[ERROR] Exception in load_msa from {str(p)}: {e}")
        return None

def load_fasta(path: str | Path, logger: Logger) -> Dict[str, str] | None:
    p = Path(path)

    try:
        header: str | None = None
        seq_parts: list[str] = []

        with p.open("r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n").strip()

                if not line:
                    continue

                if line.startswith(">"):
                    if header is not None:
                        logger.print(f"[ERROR] Multiple sequences found in FASTA file: {str(p)}")
                        return None

                    header = line[1:].strip()
                else:
                    if header is None:
                        logger.print(f"[ERROR] Invalid FASTA format in {str(p)}: sequence line appears before header.")
                        return None
                    seq_parts.append(line)

        if header is None:
            logger.print(f"[ERROR] No header found in FASTA file: {str(p)}")
            return None

        sequence = "".join(seq_parts)

        if sequence.strip() == "":
            logger.print(f"[ERROR] Empty sequence found in FASTA file: {str(p)}")
            return None

        return {"header": header, "sequence": sequence}

    except Exception as e:
        logger.print(f"[ERROR] Exception in loading FASTA from {str(p)}: {e}")
        return None

def write_msa(msa_list: List[Dict[str, str]], output_path: str | Path, logger: Logger) -> bool:
    p = Path(output_path)

    try:
        suffix = p.suffix.lower()

        if suffix in {".sto", ".stockholm"}:
            return write_sto(msa_list, p, logger)

        elif suffix in {".fa", ".fasta", ".afa"}:
            return write_aligned_fasta(msa_list, p, logger)

        elif suffix == ".a3m":
            return write_a3m(msa_list, p, logger)

        else:
            logger.print(f"[ERROR] Unsupported MSA format: {str(p)}")
            return False

    except Exception as e:
        logger.print(f"[ERROR] Exception in write_msa: {e}")
        return False

def write_hmm(sto_path: str | Path, output_path: str | Path, logger: Logger) -> bool:
    sto_file = Path(sto_path)
    hmm_file = Path(output_path)

    try:
        if not sto_file.exists():
            logger.print(f"[ERROR] Input Stockholm file not found: {str(sto_file)}")
            return False

        hmm_file.parent.mkdir(parents=True, exist_ok=True)

        p = subprocess.run(
            [
                "hmmbuild",
                "--hand",
                str(hmm_file),
                str(sto_file),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if p.returncode != 0:
            logger.print(f"[ERROR] hmmbuild failed for {str(sto_file)}: {p.stderr.strip()}")
            return False

        if (not hmm_file.exists()) or hmm_file.stat().st_size == 0:
            logger.print(f"[ERROR] Failed to generate HMM file: {str(hmm_file)}")
            return False

        return True

    except Exception as e:
        logger.print(f"[ERROR] Exception in write_hmm: {e}")
        return False

