"""the setup .py file is a essential part of packaging and distributing python project.
Its use dby the setuptools(or disutils in older python versions) to define the configuration
of your project, such as meta data version and dependiencies and meany more.
"""

from setuptools import find_packages,setup
from typing import List

# 
def get_requirements()->List[str]:
    #this function will return list of requirements
    requirement_lst=[]
    try:
        with open('requirements.txt','r') as file:
            #read the line fro file
            lines=file.readlines()
            #process each line
            for line in lines:
                requirement=line.strip()
                # ignore empty line and the -e . 
                if requirement and requirement!="-e .":
                    requirement_lst.append(requirement)
                

    except FileNotFoundError:
        print("requirements.txt file not found")
                
    return requirement_lst


## do this at last of your project
setup(
    name="Network security",
    version="0.0.1",
    author="latha K H",
    author_email="lathah2018@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()     # install the all requirements

)

