# parser.py
import requests
from bs4 import BeautifulSoup
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


GROBID_URL = "http://localhost:8070/api/processFulltextDocument"


def parse_pdf_with_grobid(pdf_path):
    logging.info(f"Starting to parse PDF: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'input': (f.name, f, 'application/pdf', {'consolidateHeader': '1'})}
            response = requests.post(GROBID_URL, files=files, timeout=45)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml-xml')
            title_tag = soup.find('title', level="a", type="main")
            title = title_tag.text.strip() if title_tag else "Title not found"

            abstract_tag = soup.find('abstract')
            abstract = abstract_tag.text.strip() if abstract_tag else "Abstract not found"

            keywords_tag = soup.find('keywords')
            keywords = [kw.text.strip() for kw in keywords_tag.find_all('term')] if keywords_tag else []

            authors = []

            header = soup.find('teiHeader')
            if header:
                author_tags = header.select('fileDesc > sourceDesc > biblStruct > monogr > author')
                for author_tag in author_tags:
                    pers_name_tag = author_tag.find('persName')
                    if not pers_name_tag: continue

                    firstname = pers_name_tag.find('forename', type='first')
                    surname = pers_name_tag.find('surname')
                    name = f"{firstname.text.strip() if firstname else ''} {surname.text.strip() if surname else ''}".strip()

                    institutions = [aff_tag.find('orgName').text.strip() for aff_tag in
                                    author_tag.find_all('affiliation') if aff_tag.find('orgName')]

                    if name:
                        authors.append({'name': name, 'institutions': institutions})

            if not authors:
                logging.warning(f"No authors found in <teiHeader> for '{title}'. Trying fallback strategy.")
                for author_tag in soup.find_all('author'):
                    if author_tag.find_parent('listBibl'):
                        continue

                    pers_name_tag = author_tag.find('persName')
                    if not pers_name_tag: continue

                    firstname = pers_name_tag.find('forename', type='first')
                    surname = pers_name_tag.find('surname')
                    name = f"{firstname.text.strip() if firstname else ''} {surname.text.strip() if surname else ''}".strip()

                    institutions = [aff_tag.find('orgName').text.strip() for aff_tag in
                                    author_tag.find_all('affiliation') if aff_tag.find('orgName')]

                    if name:
                        authors.append({'name': name, 'institutions': institutions})

            publication_info = {}
            monogr_tag = soup.find('monogr')
            if monogr_tag:
                journal_title_tag = monogr_tag.find('title', level='j')
                if journal_title_tag:
                    publication_info['name'] = journal_title_tag.text.strip()
                    publication_info['type'] = 'Journal'
                else:
                    meeting_tag = monogr_tag.find('meeting')
                    if meeting_tag and meeting_tag.find('title'):
                        publication_info['name'] = meeting_tag.find('title').text.strip()
                        publication_info['type'] = 'Conference'
                        location_tag = meeting_tag.find('addrLine')
                        publication_info['location'] = location_tag.text.strip() if location_tag else None

                date_tag = monogr_tag.find('date', type='published')
                if date_tag and date_tag.has_attr('when'):
                    publication_info['publication_date'] = date_tag['when']
                else:
                    publication_info['publication_date'] = None

            parsed_data = {
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "keywords": keywords,
                "publication_info": publication_info,
                "pdf_file_path": pdf_path
            }
            logging.info(f"Successfully parsed (Smart Strategy): {title}")
            return parsed_data
        else:
            logging.error(f"Grobid returned a non-200 status code: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        logging.error(f"Grobid request timed out for PDF: {pdf_path}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during parsing of {pdf_path}: {e}", exc_info=True)
        return None