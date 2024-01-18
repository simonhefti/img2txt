from setuptools import setup

setup(
    name='img2txtocr',
    version='0.1.0',    
    description='Extract text from PDF and images',
    author='Simon Hefti',
    author_email='simon.hefti@d-one.ai',    
    license='MIT',
    packages=['img2txtocr'],
    install_requires=['pytesseract',
                      'pillow',
                      'lingua-language-detector',
                      'nostril @ git+https://github.com/casics/nostril.git',
                      'fold_to_ascii',
                      'ftfy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'],
)