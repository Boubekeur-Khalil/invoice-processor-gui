from setuptools import setup, find_packages

setup(
    name='invoice-processor-gui',
    version='0.1.0',
    author='Boubekeur Khalil',
    author_email='khalil.beckeur@gmail.com',  # Add your email if desired
    description='A GUI application for processing invoices and extracting data into CSV format.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'paddleocr',
        'tkinter',
        'opencv-python',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'invoice-processor-gui=gui.main_window:main',
        ],
    },
)