cd /commservice/src/ 
celery -A core worker -l debug

#nohub celery flower -A core --address=0.0.0.0 --port=5555 &