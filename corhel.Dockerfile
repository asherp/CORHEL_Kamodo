FROM apembroke/kamodo:0.1

# RUN git clone https://github.com/asherp/Kamodo.git
# RUN pip install -e Kamodo

# # Keep plotly at lower api
# RUN pip install plotly==4.7.1

RUN conda install -c conda-forge pyhdf

ADD . /corhel
# RUN git clone https://github.com/asherp/kamodo.git

WORKDIR /corhel

RUN pip install -e .

CMD ["kamodo-serve"]

