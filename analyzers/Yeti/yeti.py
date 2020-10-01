#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyeti
from cortexutils.analyzer import Analyzer


class YetiAnalyzer(Analyzer):

    def __init__(self):
        Analyzer.__init__(self)
        self.url = self.get_param('config.url', None, 'Missing URL for Yeti API')
        self.api_key = self.get_param('config.api_key')
        self.verify_ssl = self.get_param("config.verify_ssl", True, None)

    def summary(self, raw):
        count = len(raw.get('findings', []))
        value = "{} hit{}".format(count, "(s)" if count > 1 else "")

        result = {
            "taxonomies": [{
                "level": "info",
                "namespace": "YETI",
                "predicate": "Search",
                "value": value
            }]
        }
        return result

    def run(self):
        api = pyeti.YetiApi("{}/api/".format(self.url), api_key=self.api_key, verify_ssl=self.verify_ssl)
        data = self.get_data()

        try:
            result = api.observable_search(value=data)

            self.report({
                'findings': result
            })
        except Exception:
            self.error('An issue occurred while calling Yeti API')


if __name__ == '__main__':
    YetiAnalyzer().run()
