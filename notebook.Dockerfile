FROM asherp/kamodo:latest
LABEL maintainer "Asher Pembroke <apembroke@predsci.com>"


# install corhel-kamodo
WORKDIR Kamodo/readers/corhel
ADD . Kamodo/readers/corhel
RUN conda install -c conda-forge pyhdf
RUN pip install -e Kamodo/readers/corhel




CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

# CMD ["jupyter", "notebook", "./docs/notebooks", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

#####
# For Jupyter notebook interaction, use:
#	docker run -p 8888:8888 dezeeuw/kamodo
# For command line interaction, use:
#	docker run -it dezeeuw/kamodo /bin/bash
#   -above, with current working directory mounted in container, use
#	docker run -it --mount type=bind,source="$(pwd)",destination=/local,consistency=cached  dezeeuw/kamodo /bin/bash
#   -above, with persistent disk space, use
#	docker run -it --mount source=kamododisk,target=/kdisk dezeeuw/kamodo /bin/bash
#
# Persistent disk space command
#	docker volume create kamododisk
#