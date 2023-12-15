import requests
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


class PsdScrapper:
    page_urls = {
        "fiscality": "https://www.psd.pt/pt/fiscalidade",
        "housing": "https://www.psd.pt/pt/habitacao",
        "inflation": "https://www.psd.pt/pt/combate-aos-efeitos-da-inflacao",
        "migration": "https://www.psd.pt/pt/imigracao",
        "elderly": "https://www.psd.pt/pt/bem-estar-da-pessoa-idosa",
        "constitutional_reform": "https://www.psd.pt/pt/revisao-constitucional",
        "births": "https://www.psd.pt/pt/natalidade",
        "education": "https://www.psd.pt/pt/educacao",
        "health": "https://www.psd.pt/pt/saude",
    }
    section_translation = {
        "fiscality": "fiscalidade",
        "housing": "habitação",
        "inflation": "inflação",
        "migration": "imigração",
        "elderly": "pessoa idosa",
        "constitutional_reform": "revisao constitucional",
        "births": "natalidade",
        "education": "educação",
        "health": "saude",
    }
    
    def __init__(self):
        self.pages_html = {}
        self.proposals = {}

    @staticmethod
    def _get_single_page(url: str) -> BeautifulSoup:
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")

    def get(self, ref: str="all") -> None:
        if ref == "all":
            for page_ref, page_url in PsdScrapper.page_urls.items():
                self.pages_html[page_ref] = PsdScrapper._get_single_page(page_url)
        elif ref in PsdScrapper.page_urls:
            self.pages_html[page_ref] = PsdScrapper._get_single_page(page_url)
        else:
            raise KeyError(f"{ref} isn't a key in dict of PSD pages") 

    @staticmethod
    def _parse_proposal_page(page: BeautifulSoup) -> str:
        all_containers = page.find_all("div", class_="container")

        proposals = []
        for container in all_containers:
            desc = container.find("div", class_="description")
            if desc:
                for br_tag in desc.find_all("br"):
                    br_tag.replace_with(' ')
                text = desc.get_text().strip().replace("\n", " ")
                text = text.replace(u'\xa0', u' ')
                proposals.append(text)
        return proposals

    def parse_proposals(self) -> None:
        for page_ref, page_soup in self.pages_html.items():
            text = PsdScrapper._parse_proposal_page(page_soup)
            self.proposals[page_ref] = text

    def to_dataframe(self) -> pd.DataFrame:
        row_proposals = []
        for page, page_proposals in self.proposals.items():
            for proposal in page_proposals:
                for term in ["Data Proposta PSD", "Data Votação"]:
                    text_split = proposal.split(term)
                    if len(text_split) > 1:
                        proposal_dict = {
                            "category": page,
                            "category_pt": PsdScrapper.section_translation[page],
                            "proposal_pt": text_split[0],
                            "votes_pt": term + text_split[1]
                        }
                        break
                else:
                    proposal_dict = {
                        "category": page,
                        "category_pt": PsdScrapper.section_translation[page],
                        "proposal_pt": text_split[0]
                    }
                row_proposals.append(proposal_dict)
        return pd.DataFrame(row_proposals)

    def to_csv(self, path: Path):
        df = self.to_dataframe()
        df.to_csv(path, sep="\t", index=False)