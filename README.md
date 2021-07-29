# Training_VMO_TwoMonth

## Run week3_week4_crawlDataCVE

### Crawl by : 
- https://nvd.nist.gov/vuln/full-listing 
- https://www.vulnerabilitycenter.com

### PYTHON VERSION
3.8

### DATABASE STRUCTURE

### Database Management System: Mongodb Enterprise 
Database name: CVE_DB
Collection name: 
- year_month_cve

> {"year" : { "bsonType": "string" }, "month" : { "bsonType": "string" }, "_id" : { "bsonType": "string" } }
`
- cve_detail:

>"_id" : { "bsonType": "string" },
>"description" : { "bsonType": "string" },
>"published_date" : { "bsonType": "string" },
>"last_modified" : { "bsonType": "string" },
>"source" : { "bsonType": "string" },
"severity" : {
	"cvss_ver_3x" : {
	    "base_score" : { "bsonType": "string" }
	},
	"cvss_ver_2" : {
	    "base_score" : { "bsonType": "string" }
	}
}
`

- cve_detail_full

"_id" : { "bsonType": "string" },
"description" : { "bsonType": "string" },
"published_date" : { "bsonType": "string" },
"last_modified" : { "bsonType": "string" },
"source" : { "bsonType": "string" },
"severity" : {
	"cvss_ver_3x" : {
	    "base_score" : { "bsonType": "string" }
	},
	"cvss_ver_2" : {
	    "base_score" : { "bsonType": "string" }
	}
},
"skybox_id" : { "bsonType": "string" },
"vendor" : { "bsonType": "string" },
"scanner" : { "bsonType": "string" },
"affected_products" : {
    "product" : { "bsonType": "string" },
    "category" : { "bsonType": "string" },
    "affected_versions" : { "bsonType": "string" }
},
"solutions" : [
    {
        "name" : { "bsonType": "string" },
        "type" : { "bsonType": "string" },
        "description" : { "bsonType": "string" }
    },
]
}


