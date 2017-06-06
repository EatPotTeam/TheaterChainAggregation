TheaterChainAggregation

the theater chain aggregation for the system analysis course



Environment

python3.5, sqlite



Setting

- If you can't update the database, maybe the api appkey from the https://www.juhe.cn/docs/api/id/42/aid/122 is no use
- you should set the envvar
  - export API_APPKEY=sfsdfjsldfjkdsjfkdsjf



Setup

- Install require package
  - pip3 install -r requirement.txt
- Run the server
  - python3 managy.py runserver
- Update the database
  - use a browser and request GET localhost:5000/api/update
