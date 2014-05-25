import os
import sys

sys.path.insert(0, os.path.dirname(__file__)+"/lib")
import scholar

import sublime
import sublime_plugin

scholar_engine = None

class ScholarEngine():
    def __init__(self):
        self.querier = scholar.ScholarQuerier()
        self.settings = scholar.ScholarSettings()

        self.settings.set_citation_format(scholar.ScholarSettings.CITFORM_BIBTEX)
        self.querier.apply_settings(self.settings)

    def make_query(self,words):
        query = scholar.SearchScholarQuery()
        query.set_words(words)
        query.set_scope(True)
        query.set_num_page_results(10)

        self.querier.send_query(query)

        return self.querier.articles

class ScholarSearchCommand(sublime_plugin.WindowCommand):
    def run(self):
        global scholar_engine
        if scholar_engine is None:
            scholar_engine = ScholarEngine()

        self.window.show_input_panel("Search Articles:", "", self.run_search, None, None);

    def make_quick_panel(self,articles):
        self.window.run_command('hide_overlay')

        def on_done(ind):
            bib = articles[ind].as_citation()+'\n'
            self.window.active_view().run_command('put_bibtex_entry',{'entry':bib}) 

        title_array = [[article.attrs['title'][0],article.attrs['byline'][0]] for article in articles]  
        self.window.show_quick_panel(title_array, on_done)

    def run_search(self,text):
        global scholar_engine
        articles = scholar_engine.make_query(text)
        self.make_quick_panel(articles)       


class PutBibtexEntryCommand(sublime_plugin.TextCommand):
    def run(self,edit,entry):
        point = self.view.sel()[0].begin()
        self.view.insert(edit, point, entry)