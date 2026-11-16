from data.rag.pdfs_api import download_all_pdfs
from data.rag.pdfs_chunking import all_pdfs_chunking
from data.rag.index_chunks import index_chunked_pdfs

def run():
    download_all_pdfs()
    all_pdfs_chunking()
    index_chunked_pdfs()

if __name__ == "__main__":
    run()