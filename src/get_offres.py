# Importation des bibliothèques nécessaires.
import os
import datetime

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs




class GetOffres:
    """
    Classe pour récupérer les offres d'emploi depuis un site web.
    """

    def __init__(self, url: str):
        self.url = url

    def fetch_offres(self) -> pd.DataFrame:
        """
        Récupère les offres d'emploi depuis la page web et les retourne sous forme de DataFrame.

        Returns:
            pd.DataFrame: DataFrame contenant les offres d'emploi.
        """
        # Ouvrir l'URL et lire le contenu HTML
        response = urlopen(self.url)
        html = bs(response, "html.parser")

        # Parser le contenu HTML avec BeautifulSoup
        # soup = bs(html, 'html.parser')

        # Trouver toutes les offres d'emploi dans le HTML
        allJobs = html.find_all('div', class_='job')

        # Extraire les informations pertinentes pour chaque offre
        # offres_data = []
        titre_offre = []
        date_offre = []
        resume_offre = []
        for job in allJobs:
            # Extraction des titres, dates et résumés des offres
            titles = job.find_all('td', {'class': 'jobLabel'})
            _ = [titre_offre.append(title.get_text()) for title in titles]
            
            date_pub = job.find_all('td', {'class': 'jobPublished'})

            if date_pub:
                date_pub = date_pub[0].get_text()
                date_offre.append(date_pub)
            
            # resumes = job.find_all('td', {'class': 'jobListLabel'})
            # resumes_contents = job.find_all('td', {'class': 'jobListValue'})
            # resumes_test = [resume.get_text() for resume in resumes]
            # resumes_content_text = [resumes_content.get_text() for resumes_content in resumes_contents]
            # resume_offre = [dict(zip(resumes_test, resumes_content_text))]

            # print("Title:", titles[0])
            # print("Date Posted:", date_posted)
            # for i in range(len(resumes_test)):
            #     print(resumes_test[i] , resumes_content_text[i])
            # print("\n")

            resumes = job.find_all('td', {'class': 'jobResume'})
            _ = [resume_offre.append(resume.get_text()) for resume in resumes]

            # Préparation des listes pour DataFrame
        # Sauvegarde des données extraites dans un fichier CSV
        output_dir = '../data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        dt = str(datetime.datetime.now())
        dfJobs = pd.DataFrame({
            'TITRE_OFFRE': titre_offre,
            'DATE_PUB_OFFRE': date_offre,
            'RESUME_OFFRE': resume_offre
        })

        dfJobs.to_csv(os.path.join(output_dir, f'jobs.csv'))

        print(f"Les données ont été sauvegardées sous {os.path.join(output_dir, f'jobs.csv')} à {dt}")
        # Convertir la liste d'offres en DataFrame
        # offres_df = pd.DataFrame(resume_offre)

        return dfJobs