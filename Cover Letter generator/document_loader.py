# loading PDF, DOCX and TXT files as LangChain Documents
def load_document(file):
    import os
    name, extension = os.path.splitext(file)

    if extension == '.pdf':
        from langchain_community.document_loaders import PyPDFLoader
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain_community.document_loaders import Docx2txtLoader
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file)
    else:
        print('Document format is not supported!')
        return None

    data = loader.load()
    return data

def directory_pdf_loader(dir_path):
    from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
    loader = PyPDFDirectoryLoader(dir_path)
    data = loader.load()
    return data

# Wikipedia Data Loader
def load_from_wikipedia(query, lang='en', load_max_docs = 2):
    from langchain.document_loaders import WikipediaLoader
    loader = WikipediaLoader(query = query, lang = lang, load_max_docs = load_max_docs)
    data = loader.load()
    return data