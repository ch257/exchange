@echo off
python scripts\get_finam_data.py settings\get_finam_data_1.ini utf-8
python scripts\get_finam_data.py settings\get_finam_data_5.ini utf-8
python scripts\get_moex_data.py settings\get_moex_data.ini utf-8

::pause