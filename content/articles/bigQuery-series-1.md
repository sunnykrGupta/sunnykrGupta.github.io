Title: Export & Load Job with MongoDB - BigQuery Part-I
Date: 2017-10-16 01:12:31
Category: Blog, Series
Tags: Google BigQuery, GCP, MongoDB, Cloud Storage, Google Cloud Platform
Author: Sunny Kr Gupta
Status: published



![Google BigQuery](/images/bq-series/part1/bquery.svg)


This blog is intended for audience who wanted to get into fundamentals of BigQuery (short for BQ) and related jobs needed to get your data inside BigQuery system.


### [Google BigQuery](https://cloud.google.com/bigquery/what-is-bigquery)

**What ?** - BigQuery is Google's fully managed, petabyte scale, low cost analytics data warehouse.

**Why ?** - BigQuery is NoOps—there is no infrastructure to manage and you don't need a database administrator—so you can focus on analyzing data to find meaningful insights, use familiar SQL, and take advantage of our pay-as-you-go model.

**How ?** - Signup to [Google Cloud platform - GCP](https://bigquery.cloud.google.com/) using your google account, start loading your data and leverage the power of this NoOps system.


----------------------------------

<br>

### Terminology in BigQuery

**Dataset**

A dataset is contained within a specific project. Datasets enable you to organize and control access to your tables. A table must belong to a dataset, so you need to create at least one dataset before loading data into BigQuery.

**Tables**

A BigQuery table contains individual records organized in rows, and a data type assigned to each column (also called a field).


**Schema**

Each Every table is defined by a schema that describes field names, types, and other information. You can specify the schema of a table during the initial table creation request, or you can create a table without a schema and declare the schema in the query or load job that first populates the table. If you need to change the schema later, you can update the schema.


---------------------------------

<br>

### Loading Data into BigQuery

In this article, we are going to use a mongoDB server to export our data and going to import into BQ. There are several other ways to import data into BQ.

<br>

#### 1. Export data from MongoDB

![MongoDB](/images/bq-series/part1/mongo-db-blog.jpeg)

In this example, i have a database in mongoDB server with name `restaurantdb` with collection name `restaurantCollection`. We are going to export using `mongoexport` binary available with mongodb server tools.

![MongoDB server](/images/bq-series/part1/mongoexport.png)

```
$ mongoexport -d restaurantdb -c restaurantCollection -o restaurant.json
```

Once export is done, we can see content of `restaurant.json` file

```
$ head -n 1 restaurant.json

{ "_id" : { "$oid" : "55f14312c7447c3da7051b26" }, \
    "URL" : "http://www.just-eat.co.uk/restaurants-cn-chinese-cardiff/menu", \
    "address" : "228 City Road", "name" : ".CN Chinese", \
    "outcode" : "CF24", "postcode" : "3JH", "type_of_food" : "Chinese" }

//pretty json
{
    "name": ".CN Chinese",
    "URL": "http://www.just-eat.co.uk/restaurants-cn-chinese-cardiff/menu",
    "outcode": "CF24",
    "postcode": "3JH",
    "address": "228 City Road",
    "_id": {
        "$oid": "55f14312c7447c3da7051b26"
    },
    "type_of_food": "Chinese"
}
```

--------------------------------

<br>

#### 2. Prepare schema for Table


Now we have our data ready in json format to be imported into BQ table. We need schema to design in order to import these records. Schema is skeleton of each field with datatype and the field not described in schema will not be imported. We have given all fields as **NULLABLE** ie, if field didn't came in any records BQ will define null value.

```
$ cat restaurantSchema.json
```

```
[
    {
        "name": "name",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "URL",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "address",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "outcode",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "postcode",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "type_of_food",
        "type": "STRING",
        "mode": "NULLABLE"
    }
]
```

Reference for schema : [https://cloud.google.com/bigquery/docs/schemas](https://cloud.google.com/bigquery/docs/schemas)

--------------------------------

<br>

#### 3. Google Cloud SDK Installation

We have schema, data ready to be imported in BQ, but in order to talk to APIs of GCP services, we need Cloud SDK to be installed in our system. We are going to use `gcloud` CLI tools in order to interact with our Cloud services running in GCP.

**Installation : ** [https://cloud.google.com/sdk/](https://cloud.google.com/sdk/)

Once installation is done, run following command to verify account setup.

```
$ gcloud auth list

$ gcloud config list
```

--------------------------------

<br>

#### 4. Create BigQuery Dataset

Go to your BigQuery in google console. [https://bigquery.cloud.google.com](https://bigquery.cloud.google.com)

Follow below instruction to create dataset.

>  **Step 1:**

![Create Dataset Step 1](/images/bq-series/part1/create-ds-1.png)


> **Step 2:**

![Create Dataset Step 2](/images/bq-series/part1/create-ds-2.png)


<br>


> To create dataset through `bq` command line interface.

```
$ bq mk -d --data_location=US   BQ_Dataset

// Verify your dataset creation
$ bq ls

    datasetId
 ----------------
  BQ_Dataset

```

**Read :** [https://cloud.google.com/bigquery/docs/datasets#create-dataset](https://cloud.google.com/bigquery/docs/datasets#create-dataset)

--------------------------------

<br>

#### 5. Load data into BigQuery

Now, my directory consists two files ie, data and schema.

```
$ tree
.
├── restaurant.json
└── restaurantSchema.json

0 directories, 2 files
```

Run command to load data into BQ.  Once you submit load job, it will take seconds to minute depends on size of data you are importing into BQ table.

```
Ex: bq load --project_id=<PROJECT-ID> --source_format=NEWLINE_DELIMITED_JSON \
    mydataset.mytable ./myfile.json ./myschema.json

$ bq load --project_id=mimetic-slate-179915   \
    --source_format=NEWLINE_DELIMITED_JSON --max_bad_records 10 \
    BQ_Dataset.Restaurant ./restaurant.json  ./restaurantSchema.json
```

`--max_bad_records 10` are additional flags to allow 10 bad records while importing your job, exceeding this value will result in import failure.

<br>

**Import through Cloud Storage**


![Cloud Storage](/images/bq-series/part1/google-cloud-storage.png)



> Another methods to import the data through `Cloud Storage`, this method is lot faster compared to above one.

**Read : ** [https://cloud.google.com/storage/docs/creating-buckets](https://cloud.google.com/storage/docs/creating-buckets
)


```
//to create Cloud storage bucket for this example.
$ gsutil mb  gs://bq-storage

//to verify bucket creation
$ gsutil ls
gs://bq-storage/
```

Now , we will upload our data `restaurant.json` to storage in bucket `gs://bq-storage/`

```
//Run command to upload
$ gsutil cp restaurant.json gs://bq-storage/restaurant.json
```

Now, we can use storage URL to import into BQ tables.

```
$ bq load --project_id=mimetic-slate-179915  \
    --source_format=NEWLINE_DELIMITED_JSON --max_bad_records 10  \
    BQ_Dataset.Restaurant \
    gs://bq-storage/restaurant.json ./restaurantSchema.json
```

<br>
<br>

After `bq load` finished, run following command to verify the table creation.
```
$ bq show BQ_Dataset.Restaurant
```

> **Output will be similar to this :**

![bq show](/images/bq-series/part1/bq-show.png)


You can also verify in bigQuery UI after hitting refresh. Visit to table and click *preview*. You will start seeing records in table.

![bq show](/images/bq-series/part1/table-preview.png)

**More into bq CLI :** [https://cloud.google.com/bigquery/bq-command-line-tool](https://cloud.google.com/storage/docs/creating-buckets
)

**More into gsutil CLI :** [https://cloud.google.com/storage/docs/quickstart-gsutil](https://cloud.google.com/storage/docs/quickstart-gsutil)


-------------------------------

<br>
<br>

### SQL Query in BQ Table

We are going to run a simple query to show the output.

```
SELECT
  name,
  address
FROM
  [mimetic-slate-179915:BQ_Dataset.Restaurant]
WHERE
  type_of_food = 'Thai'
GROUP BY
  name, address
```

![query](/images/bq-series/part1/query.png)



--------------------------------

<br>

### Conclusion

- BigQuery is a query service that allows you to run SQL-like queries against
multiple terabytes of data in a matter of seconds. The technology is one of the Google’s core technologies, like MapReduce and Bigtable, and has been used
by Google internally for various analytic tasks since 2006.
- While MapReduce is suitable for long-running batch processes such as data
mining, BigQuery is the best choice for ad hoc OLAP/BI queries that require
results as fast as possible.
- Wildcard can also be applied into Bigquery tables to expand your computations to multiple tables.
- BigQuery is the cloud-powered massively parallel
query database that provides extremely high full-scan query performance
and cost effectiveness compared to traditional data warehouse solutions
and appliances

> **Next from here:** Play around with more [functionality available in BigQuery](https://cloud.google.com/bigquery/docs/how-to) and dive into it for more computation hungry jobs.


---------------


That's all from this **series Part-I**. Hope you get basic understanding of import jobs, storage and basic outline of BigQuery from this page. I have seen power of BigQuery in my workplace to crunch 100-120 TB of data and getting results in minute or two, its really incredibly awesome. I would appreciate a feedback via comments available below and claps on medium.

##### Medium Blog : [medium.com/@sunnykrgupta](https://medium.com/@sunnykrgupta)

In next blog which is part of this series, i will be covering more into *Streaming feature available in Bigquery* to push data in BQ tables in real-time to make it available for instant query on changing dataset.



