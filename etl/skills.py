"""Rule-based skill mapping for (a) course titles and (b) job-posting skill tokens.

Both sides map into the same canonical taxonomy (dashboard/config.py) so supply and demand are comparable.
Rules are deliberately transparent keyword lists — review and extend them (BRD FR-S3).
"""
import re

# ---- courses: regex on course title -> canonical skills (a course may map to several) ----------
COURSE_RULES = {
    "Python": r"python",
    "R": r"\bin R\b|\bR programming\b",
    "SQL/Databases": r"database|structured data|relational|\bsql\b",
    "Software Engineering": r"programming|computer science|data structures|algorithm|software|object-oriented|"
                            r"mathematical computing|scripting|computational methods",
    "Machine Learning": r"machine learning|statistical learning|data mining|artificial intelligence|data analytics",
    "Deep Learning": r"deep learning|neural",
    "NLP": r"language understanding|natural language|\bnlp\b",
    "GenAI/LLM": r"generative|\bllm\b",
    "Statistics": r"statistic|probability|regression|inference",
    "Big Data/Data Eng": r"large-scale|big data|data engineering|data wrangling",
    "Data Visualization": r"visuali[sz]ation",
    "Spreadsheets": r"spreadsheet",
    "Mathematics": r"calculus|linear algebra|discrete|differential|optimization|mathematical proof|multivariate|"
                   r"multidimensional|matlab",
}
_COURSE_RE = {k: re.compile(v, re.I) for k, v in COURSE_RULES.items()}


def map_course(title: str) -> list[str]:
    return [skill for skill, rx in _COURSE_RE.items() if rx.search(title)]


# ---- postings: exact (lower-cased) skill token -> canonical skills ----------------------------
POSTING_ALIASES: dict[str, list[str]] = {}


def _add(skill, tokens):
    for t in tokens.split(","):
        POSTING_ALIASES.setdefault(t.strip(), [])
        if skill not in POSTING_ALIASES[t.strip()]:
            POSTING_ALIASES[t.strip()].append(skill)


_add("Python", "python,pandas,numpy,scipy,jupyter,pyspark,flask,django,fastapi,polars")
_add("R", "r,rshiny,shiny,rstudio,ggplot2,dplyr,tidyverse")
_add("SQL/Databases", "sql,no-sql,mongo,mysql,postgresql,postgres,sql server,mssql,oracle,nosql,mongodb,sqlite,redis,cassandra,mariadb,"
                      "dynamodb,snowflake,redshift,bigquery,db2,teradata,elasticsearch,neo4j,couchbase,sybase,"
                      "firebase,cosmos db,hbase,msaccess,access,plsql,t-sql,sqlserver,aurora,mssql server,clickhouse")
_add("Software Engineering", "java,c++,c,c#,scala,go,golang,rust,javascript,typescript,git,github,gitlab,bash,shell,"
                             "linux,unix,php,ruby,swift,kotlin,julia,perl,html,css,react,node.js,nodejs,angular,vue,"
                             "bitbucket,powershell,vb.net,objective-c,dart,fortran,cobol,assembly,lua,groovy,svn,"
                             "jira,confluence,unity,unreal,vue.js,sass,fortran,haskell,erlang,elixir,clojure")
_add("Machine Learning", "scikit-learn,sklearn,xgboost,mlflow,h2o,lightgbm,catboost,weka,dask,mlr,tidymodels,"
                         "datarobot,mlops,kubeflow,sagemaker,vertex ai,azure ml,seldon")
_add("Deep Learning", "tensorflow,pytorch,keras,mxnet,caffe,theano,jax,onnx,fastai,torch,cuda,tensorrt,lightning")
_add("NLP", "spacy,nltk,gensim,huggingface,hugging face,bert,transformers,opencv")
_add("GenAI/LLM", "gpt,chatgpt,openai,langchain,llama,llm,gemini,claude,copilot,gpt-4,gpt-3,bard,pinecone,"
                  "weaviate,chroma,faiss,rag")
_add("Statistics", "sas,spss,stata,minitab,matlab,jmp,eviews,sas/stat,statistica,octave,mathematica")
_add("Big Data/Data Eng", "spark,pyspark,hadoop,hive,pig,kafka,flink,airflow,databricks,hdfs,dbt,nifi,beam,storm,"
                          "mapreduce,impala,presto,trino,luigi,dagster,prefect,sqoop,oozie,glue,talend,informatica,"
                          "ssis,pentaho,datastage,fivetran,airbyte,delta lake,iceberg,hudi,cloudera,emr,kinesis")
_add("Cloud", "aws,azure,gcp,google cloud,s3,ec2,lambda,redshift,bigquery,snowflake,databricks,sagemaker,synapse,aurora,"
              "cloudera,oracle cloud,ibm cloud,alibaba cloud,digitalocean,heroku,openstack,vmware,emr,kinesis,glue,"
              "cosmos db,dynamodb,vertex ai,azure ml")
_add("DevOps/Containers", "docker,kubernetes,terraform,jenkins,ansible,gitlab ci,circleci,puppet,chef,helm,argocd,"
                          "travis,cicd,ci/cd,bamboo,openshift,vagrant,prometheus,grafana,splunk,datadog,nagios")
_add("BI Tools", "tableau,power bi,powerbi,looker,qlik,qlikview,qlik sense,microstrategy,cognos,ssrs,sisense,domo,"
                 "thoughtspot,dax,spotfire,sap,business objects,metabase,superset,power query,alteryx,"
                 "sharepoint,power automate,powerapps,tableau prep")
_add("Data Visualization", "matplotlib,seaborn,plotly,d3,d3.js,ggplot2,dash,bokeh,streamlit,altair,highcharts,"
                           "leaflet,gradio,qgis,arcgis,excel charts,visio")
_add("Spreadsheets", "excel,spreadsheet,spreadsheets,google sheets,sheets,vba,powerpoint,word,outlook,ms office,"
                     "microsoft office,office,msaccess,visio,smartsheet")


def map_posting_skill(token: str) -> list[str]:
    return POSTING_ALIASES.get(token.strip().lower(), [])
