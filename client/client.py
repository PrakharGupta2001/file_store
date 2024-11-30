import argparse
import requests
import os
import math

BASE_URL = "http://127.0.0.1:8000"

def upload_files(files):
    for file in files:
        with open(file, "rb") as f:
            response = requests.post(f"{BASE_URL}/files", files={"file": f})
            print(response.json())

def upload_large_file(file):
    chunk_size = 1024 * 1024  # 1 MB
    total_chunks = math.ceil(os.path.getsize(file) / chunk_size)
    with open(file, "rb") as f:
        for chunk_number in range(1, total_chunks + 1):
            chunk = f.read(chunk_size)
            response = requests.post(
                f"{BASE_URL}/files/chunk",
                files={"file": (file, chunk)},
                data={"chunk_number": chunk_number, "total_chunks": total_chunks},
            )
            print(response.json())

def list_files():
    response = requests.get(f"{BASE_URL}/files")
    print(response.json())

def delete_file(filename):
    response = requests.delete(f"{BASE_URL}/files/{filename}")
    print(response.json())

def word_analysis(limit, order):
    response = requests.get(f"{BASE_URL}/files/analysis", params={"limit": limit, "order": order})
    print(response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Store CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("files", nargs="+", help="Files to upload")

    parser_add_large = subparsers.add_parser("add-large")
    parser_add_large.add_argument("file", help="Large file to upload in chunks")

    parser_ls = subparsers.add_parser("ls", help="List stored files")

    parser_rm = subparsers.add_parser("rm")
    parser_rm.add_argument("filename", help="Filename to delete")

    parser_wc = subparsers.add_parser("wc", help="Word count and frequency analysis")
    parser_wc.add_argument("--limit", type=int, default=10, help="Number of words to show")
    parser_wc.add_argument("--order", choices=["asc", "desc"], default="desc", help="Order of frequency")

    args = parser.parse_args()
    if args.command == "add":
        upload_files(args.files)
    elif args.command == "add-large":
        upload_large_file(args.file)
    elif args.command == "ls":
        list_files()
    elif args.command == "rm":
        delete_file(args.filename)
    elif args.command == "wc":
        word_analysis(args.limit, args.order)
