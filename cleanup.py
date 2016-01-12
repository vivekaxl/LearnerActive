folders = ["Charts/", "Final_Frontier/", "Tables/"]
parent = "Results/"
for folder in folders:
    filepath = parent + folder
    from os import system
    system("rm -rf " + filepath + "*")
