from setuptools import setup,find_packages
from GameAI.__init__ import __version__

setup( name = 'GameAI',
       version = __version__,       
       author = 'Lavotap',
       author_email = 'liujiapple@hotmail.com',
       license = "GNU GENERAL PUBLIC LICENSE",
       url = 'https://github.com/lavotap/GameAI',
       download_url = 'https://codeload.github.com/lavotap/GameAI/zip/master',
       packages = ['GameAI'],
       )
