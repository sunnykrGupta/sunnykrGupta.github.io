Title: Patch and Update Table - BigQuery Part-III
Date: 2017-11-05 11:12:31
Category: Blog, Series
Tags: Google BigQuery, GCP, Google Cloud Platform
Author: Sunny Kr Gupta
Status: published
Summary: Table updation is important when you have data ready inside the table and suddenly you have a requirement of adding more fields in the table to do analysis. In this post, we are going to dive into Streaming feature of BigQuery.


![Google BigQuery](/images/bq-series/part3/bigquery.png)


This post is 3rd part of 3-post series. In the earlier post, we understood the streaming in BigQuery **[Streaming with Redis - BigQuery Part-II](https://sunnykrgupta.github.io/streaming-with-redis-bigquery-part-ii.html)**. In this post, we are going to learn patching and updating table schemas.

<br>

### Update/Patch Table in BigQuery

Table updation is important when you have data ready inside the table and suddenly you have a requirement of adding more fields in the table to do analysis.

Here, we are going to add a field and see the changes in the table after update operation.

<br>

-----------------------------

<br>

#### 1. Add field into schema

We are going to use same table **`StreamTable`** which we used earlier for streaming and introducing one more field as **`UniqueSocialNumber`** with datatype **`INTEGER`**. Lets add these changes to **`schema.py`** which will be used by our main program written in later steps.


```
$ cat schema.py

#Add field schema
TableObject = {
    "tableReference": {
      "projectId": "mimetic-slate",
      "tableId": "StreamTable",
      "datasetId": "BQ_Dataset",
    },

    "schema": {
      "fields": [
          {
              "name": "username",
              "type": "STRING",
              "mode": "NULLABLE"
          },
          {
              "name": "name",
              "type": "STRING",
              "mode": "NULLABLE"
          },
          {
              "name": "birthdate",
              "type": "STRING",
              "mode": "NULLABLE"
          },
          {
              "name": "sex",
              "type": "STRING",
              "mode": "NULLABLE"
          },
          {
              "name": "address",
              "type": "STRING",
              "mode": "NULLABLE"
          },
          {
              "name": "mail",
              "type": "STRING",
              "mode": "NULLABLE"
          },
          {
              "name": "UniqueSocialNumber",   #New Field
              "type": "INTEGER",
              "mode": "NULLABLE"
          }
      ],
  },
}
```

<br>

--------------------------------

<br>

#### 2. Patch/Update API in BigQuery


We have `schema.py` script ready and below is our main program **`tablePatch.py`** that will execute the table patch API call to bigquery.

We have two methods available in BigQuery to make updates in table.

- **`tables.patch`** - This method only replaces fields that are provided in the resources
- **`tables.update`** - This method replaces the entire table resource.

<br>

> **Patch Example :**

```
$ cat tablePatch.py

#!/usr/bin/env python

#https://developers.google.com/api-client-library/python/
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from schema import TableObject


# [START Table Creater ]
def PatchTable(bigquery):
    tables = bigquery.tables()

    tableStatusObject = tables.patch(projectId=TableObject['tableReference']['projectId'], \
                datasetId=TableObject['tableReference']['datasetId'], \
                tableId=TableObject['tableReference']['tableId'], \
                body=TableObject).execute()
    print "\n\nTable Patched"
# [END]

def main():
    #to get credentials from my laptop
    credentials = GoogleCredentials.get_application_default()
    # Construct the service object for interacting with the BigQuery API.
    bigquery = discovery.build('bigquery', 'v2', credentials=credentials)
    PatchTable(bigquery)

'''
https://cloud.google.com/bigquery/docs/tables#update-schema
'''

if __name__ == '__main__':
    main()
    print "BQ Table Patch !!"
```

<br>

> Update Example :

```
#instead of calling patch(), we call update() to apply updates
tables.update(projectId=TableObject['tableReference']['projectId'],\
                datasetId=TableObject['tableReference']['datasetId'],\
                tableId=TableObject['tableReference']['tableId'], \
                body=TableObject).execute()
```

<br>

After applying changes we can verify changes in schema of bigquery table.

Visit UI :[https://bigquery.cloud.google.com](https://bigquery.cloud.google.com)

You can also verify table schema by running **`bq`** CLI commands

```
$ bq show BQ_Dataset.StreamTable
Table mimetic-slate:BQ_Dataset.StreamTable

   Last modified                Schema               Total Rows   Total Bytes   Expiration   Time Partitioning   Labels  
 ----------------- -------------------------------- ------------ ------------- ------------ ------------------- --------
  04 Nov 15:48:43   |-username: string              451          50837                                                  
                    |-name:string                                                                                      
                    |-birthdate:string                                                                                 
                    |-sex:string                                                                                       
                    |-address:string                                                                                   
                    |-mail:string                                                                                      
                    |-UniqueSocialNumber: integer

```

<br>

**Reference ** :

- **Table Patch and Update :** [https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/bigquery_v2.tables.html](https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/bigquery_v2.tables.html)


<br>

----------------------

<br>

#### 3. Preview of data in bigquery table

Click on table preview to see new field. It will show **`null`** with old records. You can start streaming data which contains this newly added field to be written in table going forward.

<div style="text-align: center"><u><b>Table Preview</b></u></div>

![New Field](/images/bq-series/part3/new-field.png)


<br>

---------------

<br>

**Github reference** : [https://github.com/sunnykrGupta/Bigquery-series](https://github.com/sunnykrGupta/Bigquery-series)

<br>

---------------

<br>

### Conclusion

This was introduction to updation in BigQuery table, thus concludes our 3-post series.

From this series, we covered basic features of Google BigQuery serverless product. There are other similar product available on other clouds like AWS redshift, Azure SQL Data Warehouse which serve infinite computing resources like BigQuery.

Please comment your thoughts/feedback about this series.

---------------
