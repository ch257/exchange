@echo off
python scripts\concatinate_data.py settings\concatinate_data_Si.ini utf-8
python scripts\concatinate_data.py settings\concatinate_data_Eu.ini utf-8
python scripts\concatinate_data.py settings\concatinate_data_ED.ini utf-8

pause