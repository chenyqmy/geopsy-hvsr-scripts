"""
This script is used to process ambient noise seismic data using the HVSR method. Geopsy is used as a command line tool to process the data. Multiprocessing is used to speed up the process.

author: Chen Yu-Qiao
date: 2023-03-26
"""

import subprocess
from multiprocessing import Pool
import datetime
from obspy import read
from TraceSelect import TraceSelect
import os
from concurrent.futures import ThreadPoolExecutor


# 1. We need to make a date list to represent data for each day
start = datetime.datetime.strptime("20120201", "%Y%m%d")
end = datetime.datetime.strptime("20120210", "%Y%m%d")
date_generated = [
    start + datetime.timedelta(days=x) for x in range(0, (end - start).days)
]

date_list = []
for date in date_generated:
    date_list.append(date.strftime("%Y%m%d"))


# 2. Define a function to produce temporary mseed data for each geopsy command to run and save output to a folder
def do_hvsr(station, date):
    """Use geopsy-hv command line tool to produce hvsr file"""

    print(f"processing {station} {date}")
    try:
        st = read(f"../{station}/*_{date}*_*.mseed")
        st = TraceSelect(st)
        # print(st)
        file_name = f"{station}_{date}_temp_file_for_hvsr_calc.mseed"
        st.write(file_name)

        folder_name = f"{station}_output"
        if not os.path.exists(folder_name):  # create a folder to store output files
            os.mkdir(folder_name)

        # create a temp_folder to store the output files from geopsy-hv
        temp_folder = f"{station}_{date}_temp_folder"
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)

        subprocess.run(
            ["geopsy-hv", file_name, "-param", "params", "-o", temp_folder],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )  # run geopsy-hv command line tool

        os.remove(file_name)  # remove temporary mseed file in folder

        # rename and move the files in temp_folder
        os.rename(
            f"{temp_folder}/XC_{station}.hv", f"{folder_name}/{station}_{date}.hv"
        )
        os.rename(
            f"{temp_folder}/XC_{station}.log", f"{folder_name}/{station}_{date}.log"
        )

        # remove temp_folder and files in it
        os.rmdir(temp_folder)

    except:
        print(f"no data for {station} {date}")


if __name__ == "__main__":
    stations = ["PIG1", "PIG2", "PIG3", "PIG4"]  # staions list this is foldername of your data
    with ThreadPoolExecutor() as executor:
        for station in stations:
            for date in date_list:
                executor.submit(do_hvsr, station, date)