/**
 * Posts Data Management. Enhanced with analytics, categories, trending, and featured flags
 */

window.posts = {
  'first-post': {
    title: 'Welcome to My Technical Blog',
    date: 'June 5, 2026',
    publishedAt: new Date('2026-06-05').getTime(),
    readTime: 5,
    tags: ['Introduction', 'Data Engineering', 'Career'],
    category: 'Career',
    isDraft: false,
    featured: true,
    excerpt: 'Welcome to my technical blog where I document real-world data engineering patterns, ETL pipeline architectures, and lessons learned building production data systems. In this inaugural post, I share my journey into data engineering, the challenges of working with messy real-world data, and the core principles that guide my approach to building reliable, scalable data infrastructure. Whether you are transitioning into data engineering or looking to sharpen your skills, this blog covers everything from Apache Airflow DAG design to Kubernetes deployment strategies for data workloads.',
    views: 1240,
    likes: 89,
    shares: 34,
    comments: 12,
    image: 'assets/images/1.jpeg',
    content: '<p>Welcome to my technical blog! I\'m Victor Kipruto Rop, a Data Engineer passionate about building scalable, production-grade data systems.</p>'
  },
  'data-engineering': {
    title: 'Data Engineering Fundamentals: Building Scalable Systems',
    date: 'June 4, 2026',
    publishedAt: new Date('2026-06-04').getTime(),
    readTime: 12,
    tags: ['Data Engineering', 'Architecture', 'Best Practices', 'Python', 'SQL'],
    category: 'Data Engineering',
    isDraft: false,
    featured: true,
    excerpt: 'A comprehensive deep dive into data engineering fundamentals that every practitioner needs to master. This guide covers the full spectrum of data architecture principles including Lambda and Kappa architectures, the modern data stack with tools like dbt, Airflow, and Spark, ETL versus ELT design patterns, data modeling techniques (star schema, snowflake, Data Vault), and strategies for building scalable data warehouses on Snowflake, BigQuery, and Redshift. Includes practical code examples, real-world case studies, and battle-tested patterns from production environments processing terabytes of data daily.',
    views: 3450,
    likes: 234,
    shares: 89,
    comments: 45,
    image: 'assets/images/2.jpeg',
    content: '<p>Data engineering is the backbone of modern data-driven organizations.</p>'
  },
  'airflow-advanced': {
    title: 'Advanced Airflow Patterns & Optimization',
    date: 'May 28, 2026',
    publishedAt: new Date('2026-05-28').getTime(),
    readTime: 14,
    tags: ['Apache Airflow', 'Orchestration', 'Advanced', 'Docker'],
    category: 'Data Engineering',
    isDraft: false,
    featured: false,
    excerpt: 'Master advanced Apache Airflow patterns that go beyond basic DAG construction. This comprehensive guide covers dynamic DAG generation using factory patterns, custom operators for domain-specific data tasks, sensor patterns for event-driven workflows, the TaskFlow API for Python-native task composition, and sophisticated scheduling with time sensors and external task triggers. Learn how to implement cross-DAG dependencies, handle late-arriving data with backfill strategies, optimize pool and queue configurations for large-scale deployments, and monitor Airflow health with Prometheus and Grafana dashboards. Includes production-ready code snippets from pipelines processing over 50 million records daily.',
    views: 2100,
    likes: 156,
    shares: 67,
    comments: 23,
    image: 'assets/images/airflow-pipelines.png',
    content: '<p>As your data infrastructure matures, basic Airflow DAGs become insufficient.</p>'
  },
  'kafka-streaming': {
    title: 'Real-time Event Streaming with Kafka and Python',
    date: 'May 15, 2026',
    publishedAt: new Date('2026-05-15').getTime(),
    readTime: 11,
    tags: ['Kafka', 'Streaming', 'Python', 'Real-Time'],
    category: 'Data Engineering',
    isDraft: false,
    featured: true,
    excerpt: 'A thorough exploration of building real-time event streaming applications with Apache Kafka and Python. This article covers Kafka architecture fundamentals including brokers, topics, partitions, and consumer groups, then dives deep into implementing Python producers with serialization strategies (Avro, Protobuf, JSON Schema), exactly-once semantics with idempotent producers, and consumer group patterns for parallel processing. Learn stream processing with Kafka Streams and ksqlDB, implement the outbox pattern for reliable event publishing, handle schema evolution with Confluent Schema Registry, and monitor throughput with Kafka metrics and Grafana dashboards. Real-world examples from building a real-time analytics pipeline processing 2 million events per minute.',
    views: 1890,
    likes: 142,
    shares: 56,
    comments: 18,
    image: 'assets/images/3.jpeg',
    content: '<p>Kafka has become synonymous with real-time data pipelines.</p>'
  },
  'dbt-fundamentals': {
    title: 'dbt (Data Build Tool): SQL-First Data Transformation',
    date: 'April 30, 2026',
    publishedAt: new Date('2026-04-30').getTime(),
    readTime: 9,
    tags: ['dbt', 'SQL', 'Transformation', 'Data Engineering'],
    category: 'Data Engineering',
    isDraft: false,
    featured: false,
    excerpt: 'Get started with dbt (data build tool) for version-controlled, tested SQL transformations that bring software engineering rigor to analytics. This guide covers project structure best practices, model materialization strategies (view, table, incremental, ephemeral), testing frameworks for data quality assertions, documentation generation, and Jinja macro patterns for DRY transformations. Learn how to implement surrogate keys, handle slowly changing dimensions, build recursive CTE hierarchies, configure incremental models with merge strategies, and set up dbt packages from the Hub. Includes a complete end-to-end example building a data warehouse with Kimball-style dimensional models, comprehensive test suites, and automated documentation.',
    views: 1560,
    likes: 98,
    shares: 42,
    comments: 15,
    image: 'assets/images/dbt-best-practices.png',
    content: '<p>dbt has fundamentally changed how data teams approach transformations.</p>'
  },
  'snowflake-performance': {
    title: 'Snowflake Query Optimization & Cost Management',
    date: 'April 12, 2026',
    publishedAt: new Date('2026-04-12').getTime(),
    readTime: 10,
    tags: ['Snowflake', 'Performance', 'Cloud', 'Cost Optimization'],
    category: 'Cloud',
    isDraft: false,
    featured: false,
    excerpt: 'Techniques for optimizing Snowflake queries, reducing compute costs by up to 60%, and leveraging materialized views for sub-second analytics. This deep dive covers query profiling with the Snowflake query history, identifying and resolving data skew in large joins, optimizing warehouse sizing with multi-cluster auto-scaling, implementing result caching strategies, and using search optimization services for point lookups. Learn how to design efficient clustering keys, choose between materialized views and dynamic tables, implement zero-copy cloning for dev/test environments, and use Snowflake performance insights to right-size your compute resources. Includes cost analysis frameworks and ROI calculations from real production deployments.',
    views: 1340,
    likes: 87,
    shares: 31,
    comments: 9,
    image: 'assets/images/4.jpeg',
    content: '<p>Snowflake\'s pay-as-you-go model makes cost optimization critical.</p>'
  },
  'micro-1': {
    title: 'The Modern Microservices Guide for Data Engineers',
    date: 'June 7, 2026',
    publishedAt: new Date('2026-06-07').getTime(),
    readTime: 15,
    tags: ['Microservices', 'Architecture', 'Data Engineering', 'Kubernetes'],
    category: 'Architecture',
    isDraft: false,
    featured: true,
    excerpt: 'How to design, deploy, and monitor microservices in a data-intensive environment with practical patterns for service decomposition, API gateway configuration, and distributed tracing. This guide covers domain-driven design for identifying service boundaries, implementing the saga pattern for distributed transactions across data services, building event-driven architectures with NATS and gRPC, configuring service mesh with Istio for traffic management and security, and setting up comprehensive observability with OpenTelemetry traces, Prometheus metrics, and structured logging. Learn container orchestration strategies, rolling deployment patterns, canary releases, and blue-green deployments specifically tailored for data processing microservices handling millions of daily transactions.',
    views: 2890,
    likes: 198,
    shares: 78,
    comments: 34,
    image: 'assets/images/kubernetes-patterns.png',
    content: '<p>Microservices have revolutionized how we build scalable applications.</p>'
  },
  'analytics-1': {
    title: 'Real-Time Analytics at Scale',
    date: 'June 6, 2026',
    publishedAt: new Date('2026-06-06').getTime(),
    readTime: 12,
    tags: ['Analytics', 'Real-Time', 'Infrastructure', 'Python'],
    category: 'Analytics',
    isDraft: false,
    featured: false,
    excerpt: 'Building low-latency analytics systems that process millions of events per second using ClickHouse, Apache Druid, and real-time aggregation patterns. This article covers the architecture of OLAP engines, choosing between columnar stores for different query patterns, implementing materialized views for pre-aggregation, designing time-series data models for fast drill-downs, and building real-time dashboards with WebSocket connections. Learn how to implement approximate query processing with HyperLogLog sketches, build funnel analysis engines, create cohort analysis pipelines, and handle high-cardinality dimensions efficiently. Includes benchmarking results comparing query latency across different engines and deployment topologies from production analytics platforms.',
    views: 1780,
    likes: 134,
    shares: 52,
    comments: 21,
    image: 'assets/images/5.jpeg',
    content: '<p>The demand for real-time insights is growing rapidly.</p>'
  },
  'sql-1': {
    title: 'Advanced SQL Optimization for Data Warehousing',
    date: 'June 5, 2026',
    publishedAt: new Date('2026-06-05').getTime(),
    readTime: 10,
    tags: ['SQL', 'Optimization', 'Data Warehouse', 'Performance'],
    category: 'Data Engineering',
    isDraft: false,
    featured: false,
    excerpt: 'Master the art of writing high-performance SQL with advanced window functions, CTE optimization, and execution plan analysis that transforms slow queries into lightning-fast operations. This comprehensive guide covers ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, and running aggregates for complex analytical queries, recursive CTEs for hierarchical data traversal, lateral joins for correlated subqueries, and pivot/unpivot patterns for data reshaping. Learn to read and interpret EXPLAIN plans to identify bottlenecks, implement index strategies for covering queries, use partition pruning effectively, and apply query rewriting techniques that reduce execution time by orders of magnitude. Includes 20+ real-world query optimization examples with before-and-after performance comparisons.',
    views: 2340,
    likes: 176,
    shares: 63,
    comments: 28,
    image: 'assets/images/1.jpeg',
    content: '<p>SQL is the lingua franca of data.</p>'
  },
  'cloud-1': {
    title: 'Cloud Infrastructure Best Practices',
    date: 'June 4, 2026',
    publishedAt: new Date('2026-06-04').getTime(),
    readTime: 10,
    tags: ['Cloud', 'Infrastructure', 'DevOps', 'AWS'],
    category: 'Cloud',
    isDraft: false,
    featured: false,
    excerpt: 'Essential patterns for building resilient and scalable cloud infrastructure on AWS, GCP, and Azure. This guide covers multi-region deployment strategies for disaster recovery, infrastructure as Code with Terraform and Pulumi for reproducible environments, cost optimization techniques that can reduce cloud bills by 40%, security best practices including VPC design, IAM policies, and encryption at rest and in transit. Learn implementing auto-scaling groups for variable workloads, configuring load balancers with health checks and circuit breakers, building CI/CD pipelines with GitHub Actions and ArgoCD, and monitoring infrastructure with CloudWatch, Datadog, and PagerDuty. Includes real-world architectures from startups to enterprise-scale deployments processing petabytes.',
    views: 1120,
    likes: 78,
    shares: 29,
    comments: 11,
    image: 'assets/images/2.jpeg',
    content: '<p>Building in the cloud requires a shift in mindset.</p>'
  },
  'python-1': {
    title: 'Python Performance Optimization',
    date: 'June 3, 2026',
    publishedAt: new Date('2026-06-03').getTime(),
    readTime: 15,
    tags: ['Python', 'Performance', 'Data Processing', 'Best Practices'],
    category: 'Best Practices',
    isDraft: false,
    featured: false,
    excerpt: 'Advanced techniques for making your Python code run faster using multiprocessing, async patterns, and efficient memory management that can achieve 10-100x speedups on data processing workloads. This deep dive covers the Global Interpreter Lock (GIL) and when to use multiprocessing versus threading, async/await patterns for I/O-bound operations with aiohttp and asyncio, Cython and Numba for CPU-bound numerical computations, memory profiling with tracemalloc and memory_profiler, and efficient data structures using arrays, deque, and slots. Learn vectorized operations with NumPy and Pandas that replace slow Python loops, implement connection pooling for database operations, use generators for memory-efficient processing of large datasets, and apply profiling tools to identify and eliminate performance bottlenecks in production code.',
    views: 1890,
    likes: 145,
    shares: 58,
    comments: 19,
    image: 'assets/images/python-optimization.png',
    content: '<p>Python is often criticized for being slow, but with the right techniques...</p>'
  },
  'docker-1': {
    title: 'Docker and Kubernetes Deep Dive',
    date: 'June 2, 2026',
    publishedAt: new Date('2026-06-02').getTime(),
    readTime: 18,
    tags: ['Docker', 'Kubernetes', 'Containers', 'DevOps'],
    category: 'DevOps',
    isDraft: false,
    featured: true,
    excerpt: 'Containerization strategies for modern data platforms that go beyond basic Dockerfile creation. From building optimized multi-stage images that reduce size by 70% to orchestrating complex multi-container data pipelines with Docker Compose and Kubernetes. This comprehensive guide covers Docker best practices including layer caching, .dockerignore optimization, non-root user security, and health check configurations. Learn Kubernetes deployment patterns for data workloads including StatefulSets for databases, DaemonSets for log collection, Jobs and CronJobs for batch processing, and PersistentVolumes for stateful data. Implement secrets management with Sealed Secrets, configure resource limits and requests for data-heavy containers, and set up monitoring with Prometheus operator and Kubernetes dashboards.',
    views: 2560,
    likes: 189,
    shares: 72,
    comments: 31,
    image: 'assets/images/kubernetes-patterns.png',
    content: '<p>Containers are the unit of deployment for modern data systems.</p>'
  },

  /* ═══════════════════════════════════════════════════════════════════
     NEW DETAILED BLOG POSTS. June 2026
     ═══════════════════════════════════════════════════════════════════ */

  'medallion-architecture-delta-lake': {
    title: 'Building a Medallion Architecture with Delta Lake and Apache Spark',
    date: 'June 8, 2026',
    publishedAt: new Date('2026-06-08').getTime(),
    readTime: 18,
    tags: ['Delta Lake', 'Apache Spark', 'Medallion Architecture', 'Data Lakehouse', 'PySpark'],
    category: 'Data Engineering',
    isDraft: false,
    featured: true,
    trending: true,
    excerpt: 'A comprehensive deep dive into implementing the Medallion (Bronze-Silver-Gold) architecture pattern using Delta Lake and Apache Spark. Learn how to structure your data lakehouse into curated layers that progressively improve data quality, enforce schema evolution, and enable time-travel queries. This guide covers the full implementation from ingesting raw JSON and CSV files into the Bronze layer, applying cleansing rules and deduplication in the Silver layer, to building aggregate business-ready tables in the Gold layer. Includes production patterns for handling late-arriving data, managing Delta Lake transactions, optimizing file sizes with Z-Ordering and compaction, and integrating with downstream BI tools and ML pipelines.',
    views: 3200,
    likes: 245,
    shares: 95,
    comments: 38,
    image: 'assets/images/cloud-infrastructure.png',
    content: `
      <h2>Why the Medallion Architecture?</h2>
      <p>As data teams scale from handling megabytes to terabytes of daily ingestion, the flat data lake approach quickly becomes unmanageable. Data arrives in inconsistent formats, quality degrades over time, and downstream consumers lose trust in the pipeline outputs. The <strong>Medallion Architecture</strong>, also known as the Bronze-Silver-Gold pattern, solves this by introducing explicit, progressive layers of data refinement.</p>
      <p>Originally popularized by Databricks, this architecture has become the de facto standard for building lakehouse platforms. Each layer serves a distinct purpose:</p>
      <ul>
        <li><strong>Bronze Layer:</strong> Raw, immutable data as-is from the source system. This is your system of record.</li>
        <li><strong>Silver Layer:</strong> Cleansed, conformed, and deduplicated data with enforced schemas.</li>
        <li><strong>Gold Layer:</strong> Business-level aggregates optimized for analytics and reporting.</li>
      </ul>

      <h2>Setting Up Delta Lake with Spark</h2>
      <p>Delta Lake sits on top of your existing data lake storage (S3, ADLS, GCS) and adds ACID transactions, schema enforcement, and time travel on top of Parquet files. Here's how to initialize a Spark session with Delta Lake support:</p>
      <pre><code>from pyspark.sql import SparkSession

spark = (SparkSession.builder
    .appName("MedallionArchitecture")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", 
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "false")
    .getOrCreate())</code></pre>

      <h2>The Bronze Layer: Ingesting Raw Data</h2>
      <p>The Bronze layer is where all raw data lands. The key principle here is <strong>append-only, schema-on-read</strong>. You capture everything exactly as it arrives. No transformations, no filtering. This gives you a complete audit trail and the ability to reprocess from scratch if needed.</p>
      <pre><code># Bronze layer ingestion. Raw JSON events
from pyspark.sql.functions import current_timestamp, input_file_name

raw_events = (spark.read
    .format("json")
    .option("multiLine", "true")
    .load("/mnt/sources/events/streaming/"))

bronze_df = (raw_events
    .withColumn("_ingested_at", current_timestamp())
    .withColumn("_source_file", input_file_name())
    .withColumn("_event_date", 
        F.to_date(F.col("timestamp"))))

(bronze_df.write
    .format("delta")
    .mode("append")
    .partitionBy("_event_date")
    .save("/mnt/lakehouse/bronze/events"))</code></pre>

      <h3>Bronze Layer Best Practices</h3>
      <ul>
        <li>Always add metadata columns: <code>_ingested_at</code>, <code>_source_file</code>, <code>_event_date</code></li>
        <li>Partition by date for efficient data pruning and retention management</li>
        <li>Use append-only mode. Never overwrite Bronze data</li>
        <li>Enable Delta Lake change data feed (CDF) for downstream lineage tracking</li>
      </ul>

      <h2>The Silver Layer: Cleansing and Conforming</h2>
      <p>The Silver layer applies business rules to produce a clean, validated dataset. This is where you enforce schemas, remove duplicates, handle null values, and conform data from multiple sources into a unified model.</p>
      <pre><code># Silver layer. Deduplicate and cleanse
from pyspark.sql.window import Window

# Read from Bronze
bronze_events = spark.read.format("delta").load("/mnt/lakehouse/bronze/events")

# Define window for deduplication
dedup_window = Window.partitionBy("event_id").orderBy(F.desc("_ingested_at"))

silver_events = (bronze_events
    .withColumn("_row_num", F.row_number().over(dedup_window))
    .filter(F.col("_row_num") == 1)
    .drop("_row_num")
    .filter(F.col("event_id").isNotNull())
    .filter(F.col("timestamp").isNotNull())
    .withColumn("event_type", F.upper(F.col("event_type")))
    .withColumn("processed_at", current_timestamp()))

# Write with merge for idempotent processing
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/mnt/lakehouse/silver/events")

(delta_table.alias("target")
    .merge(silver_events.alias("source"),
           "target.event_id = source.event_id")
    .whenMatchedUpdateAll()
    .whenNotInsertAll()
    .execute())</code></pre>

      <h2>The Gold Layer: Business Aggregates</h2>
      <p>The Gold layer contains business-ready aggregates that power dashboards, reports, and ML features. These tables are optimized for query performance with materialized aggregates, pre-computed joins, and appropriate partitioning strategies.</p>
      <pre><code># Gold layer. Daily revenue aggregation
silver_orders = spark.read.format("delta").load("/mnt/lakehouse/silver/orders")
silver_products = spark.read.format("delta").load("/mnt/lakehouse/silver/products")

gold_daily_revenue = (silver_orders
    .join(silver_products, "product_id", "left")
    .groupBy(
        F.to_date("order_date").alias("date"),
        F.col("category"),
        F.col("region")
    )
    .agg(
        F.sum("amount").alias("total_revenue"),
        F.count("order_id").alias("order_count"),
        F.avg("amount").alias("avg_order_value"),
        F.countDistinct("customer_id").alias("unique_customers")
    ))

(gold_daily_revenue.write
    .format("delta")
    .mode("overwrite")
    .partitionBy("date")
    .save("/mnt/lakehouse/gold/daily_revenue"))</code></pre>

      <h2>Advanced Patterns: Time Travel and Schema Evolution</h2>
      <p>One of Delta Lake's most powerful features is <strong>time travel</strong>. The ability to query any historical version of your data. Combined with schema evolution, this makes the Medallion architecture incredibly resilient:</p>
      <pre><code># Query data as it was 3 days ago
historical_df = (spark.read
    .format("delta")
    .option("versionAsOf", "2026-06-05")
    .load("/mnt/lakehouse/silver/events"))

# Schema evolution. Add new columns safely
new_events = spark.read.json("/mnt/sources/new_events_v2/")
(new_events.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .save("/mnt/lakehouse/bronze/events"))</code></pre>

      <h2>Performance Optimization</h2>
      <p>To keep your lakehouse performant at scale, implement these optimization strategies:</p>
      <ul>
        <li><strong>Z-Ordering:</strong> Co-locate related data for faster point lookups. Apply Z-Order on columns commonly used in WHERE clauses.</li>
        <li><strong>VACUUM:</strong> Remove old file versions to reclaim storage. Set a retention period (e.g., 168 hours) and run VACUUM on a schedule.</li>
        <li><strong>Auto-Optimize:</strong> Enable automatic file compaction to maintain optimal file sizes (target: 128MB-1GB per file).</li>
        <li><strong>Liquid Clustering:</strong> The next evolution beyond partitioning. Automatically organizes data based on query patterns.</li>
      </ul>

      <h2>Conclusion</h2>
      <p>The Medallion Architecture provides a proven, scalable framework for building lakehouse platforms that teams can trust. By separating concerns into Bronze, Silver, and Gold layers, you create clear data contracts, enable parallel development across teams, and build a foundation that scales from gigabytes to petabytes. Combined with Delta Lake's ACID guarantees and time-travel capabilities, this pattern eliminates the "data swamp" problem and brings warehouse-level reliability to your data lake.</p>
    `
  },

  'kafka-connect-integration-guide': {
    title: 'Mastering Apache Kafka Connect: The Complete Integration Guide',
    date: 'June 7, 2026',
    publishedAt: new Date('2026-06-07').getTime(),
    readTime: 16,
    tags: ['Kafka', 'Kafka Connect', 'Streaming', 'Integration', 'ETL'],
    category: 'Data Engineering',
    isDraft: false,
    featured: true,
    trending: true,
    excerpt: 'A complete guide to Apache Kafka Connect. The framework for building scalable, fault-tolerant data integration pipelines between Kafka and external systems without writing a single line of consumer/producer code. Learn how to configure source connectors for PostgreSQL, MySQL, and MongoDB, sink connectors for Elasticsearch, S3, and Snowflake, and master Single Message Transforms (SMTs) for real-time data shaping. Covers exactly-once delivery semantics, dead letter queues, schema registry integration, monitoring with JMX metrics, and production deployment strategies for standalone and distributed modes. Includes battle-tested configurations from processing over 100 million records daily in production environments.',
    views: 2780,
    likes: 203,
    shares: 82,
    comments: 27,
    image: 'assets/images/kafka-streaming.png',
    content: `
      <h2>Why Kafka Connect?</h2>
      <p>Every data engineering team eventually faces the same challenge: moving data between systems reliably. You might need to replicate PostgreSQL CDC events to Elasticsearch, stream application logs to S3 for archival, or push real-time metrics to InfluxDB. The naive approach, writing custom Kafka producers and consumers for each integration, leads to duplicated effort, inconsistent error handling, and maintenance nightmares.</p>
      <p><strong>Kafka Connect</strong> solves this with a framework-based approach. It provides a standard interface for connecting Kafka to external systems, with built-in support for fault tolerance, offset management, schema evolution, and parallelism. You configure connectors declaratively, and the framework handles the hard parts.</p>

      <h2>Core Concepts</h2>
      <ul>
        <li><strong>Connector:</strong> A plugin that defines how to move data to or from a specific system (e.g., PostgreSQL, S3, Elasticsearch).</li>
        <li><strong>Task:</strong> The unit of parallelism. A connector can split work into multiple tasks.</li>
        <li><strong>Worker:</strong> The JVM process that runs connectors and tasks. Workers form a cluster for distributed mode.</li>
        <li><strong>Converter:</strong> Handles serialization/deserialization of data (JSON, Avro, Protobuf).</li>
        <li><strong>Transform (SMT):</strong> Lightweight single-message transformations applied in-flight.</li>
      </ul>

      <h2>Source Connector: PostgreSQL CDC</h2>
      <p>The Debezium PostgreSQL connector uses logical replication to capture every INSERT, UPDATE, and DELETE in real-time with minimal impact on the source database:</p>
      <pre><code>{
  "name": "postgres-cdc-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "prod-db.example.com",
    "database.port": "5432",
    "database.user": "kafka_connect",
    "database.password": "\${secrets:db-password}",
    "database.dbname": "production",
    "database.server.name": "prod",
    "schema.include.list": "public",
    "table.include.list": "public.orders,public.customers,public.products",
    "plugin.name": "pgoutput",
    "slot.name": "kafka_connect_slot",
    "publication.name": "kafka_connect_pub",
    "snapshot.mode": "initial",
    "heartbeat.interval.ms": "10000",
    "tombstones.on.delete": "true",
    "transforms": "route,unwrap",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
    "transforms.route.replacement": "cdc.$3",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "true",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",
    "errors.tolerance": "all",
    "errors.deadletterqueue.topic.name": "dlq-postgres-cdc",
    "errors.deadletterqueue.topic.replication.factor": "3"
  }
}</code></pre>

      <h2>Sink Connector: Elasticsearch</h2>
      <p>Push transformed events from Kafka into Elasticsearch for full-text search and real-time analytics:</p>
      <pre><code>{
  "name": "elasticsearch-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "topics": "cdc.orders,cdc.customers",
    "connection.url": "http://elasticsearch:9200",
    "type.name": "_doc",
    "key.ignore": "false",
    "schema.ignore": "false",
    "write.method": "upsert",
    "behavior.on.null.values": "delete",
    "behavior.on.malformed.documents": "warn",
    "transforms": "extractKey",
    "transforms.extractKey.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
    "transforms.extractKey.field": "id",
    "batch.size": 500,
    "max.buffered.records": 10000,
    "linger.ms": 5,
    "flush.timeout.ms": 10000,
    "max.retries": 5,
    "retry.backoff.ms": 500
  }
}</code></pre>

      <h2>Single Message Transforms (SMTs)</h2>
      <p>SMTs let you reshape records in-flight without writing custom code. Chain multiple transforms for powerful data shaping:</p>
      <pre><code>// Chain of transforms for field masking and routing
"transforms": "maskEmail,addTimestamp,route",
"transforms.maskEmail.type": "org.apache.kafka.connect.transforms.MaskField$Value",
"transforms.maskEmail.fields": "email,phone",
"transforms.maskEmail.replacement": "***REDACTED***",
"transforms.addTimestamp.type": "org.apache.kafka.connect.transforms.InsertField$Value",
"transforms.addTimestamp.timestamp.field": "_processed_at",
"transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
"transforms.route.regex": "(.+)",
"transforms.route.replacement": "enriched.\${1}"</code></pre>

      <h2>Exactly-Once Delivery</h2>
      <p>Combining Kafka Connect's offset management with idempotent sink operations achieves effectively exactly-once delivery:</p>
      <ul>
        <li>Enable <code>errors.tolerance: all</code> for fault tolerance</li>
        <li>Use idempotent writes (upserts) in sink connectors</li>
        <li>Configure <code>commit.policy</code> for periodic offset commits</li>
        <li>Leverage Kafka transactions with <code>producer.ackcks=all</code></li>
      </ul>

      <h2>Monitoring and Alerting</h2>
      <p>Monitor connector health through JMX metrics and set up alerts for production reliability:</p>
      <pre><code># Key metrics to monitor
connect.connect-metrics:type=connector-metrics,connector=<name>
  → connector-status          (RUNNING / FAILED / PAUSED)
  → task-failed               (count)
  → records-lag-max           (consumer lag)

connect.connect-metrics:type=task-metrics,connector=<name>,task=<id>
  → source-record-poll-total  (throughput)
  → source-record-write-total (write rate)
  → batch-size-avg            (batch efficiency)
  → record-error-rate         (error rate)</code></pre>

      <h2>Conclusion</h2>
      <p>Kafka Connect eliminates the need to build and maintain custom integration code. With 200+ community connectors covering virtually every database, file system, and SaaS platform, it's the fastest path to building a reliable data integration layer. Combined with Schema Registry for data governance, SMTs for lightweight transformations, and distributed mode for fault tolerance, Kafka Connect is an essential tool in any modern data engineering stack.</p>
    `
  },

  'terraform-data-platform': {
    title: 'Infrastructure as Code: Terraform Patterns for Data Platforms',
    date: 'June 6, 2026',
    publishedAt: new Date('2026-06-06').getTime(),
    readTime: 14,
    tags: ['Terraform', 'Infrastructure as Code', 'AWS', 'Cloud', 'DevOps'],
    category: 'DevOps',
    isDraft: false,
    featured: false,
    trending: true,
    excerpt: 'A practical guide to building reproducible, version-controlled data infrastructure using Terraform. Learn how to modularize your Terraform code for data platforms including VPCs, EKS clusters, RDS instances, S3 data lakes, Glue catalogs, and EMR clusters. This guide covers workspace management for multi-environment deployments, state file locking with DynamoDB, secrets management with AWS Secrets Manager, and CI/CD integration with GitHub Actions. Includes production patterns for managing Snowflake resources, Databricks workspaces, and Airflow deployments as code, with real-world module structures from infrastructure managing 50+ AWS accounts.',
    views: 1950,
    likes: 148,
    shares: 61,
    comments: 19,
    image: 'assets/images/cloud-infrastructure.png',
    content: `
      <h2>Why Terraform for Data Infrastructure?</h2>
      <p>Data infrastructure is uniquely complex. You're managing compute clusters, storage systems, networking, IAM policies, monitoring, and orchestration, all of which need to work together seamlessly. Manual configuration leads to drift, undocumented changes, and environment inconsistencies that cause production incidents.</p>
      <p><strong>Terraform</strong> treats infrastructure as code, giving you version control, peer review, automated testing, and reproducible deployments across environments. For data platforms specifically, Terraform's declarative approach ensures your infrastructure always matches your desired state.</p>

      <h2>Project Structure for Data Platforms</h2>
      <p>Organize your Terraform code into reusable modules that map to data platform components:</p>
      <pre><code>terraform/
├── modules/
│   ├── networking/          # VPC, subnets, security groups
│   ├── eks/                 # Kubernetes cluster
│   ├── rds/                 # PostgreSQL, MySQL
│   ├── s3/                  # Data lake buckets
│   ├── glue/                # Data catalog, crawlers
│   ├── emr/                 # Spark clusters
│   ├── iam/                 # Roles, policies
│   └── monitoring/          # CloudWatch, Grafana
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── shared/                  # Shared services (DNS, accounts)
└── ci/                      # Pipeline configurations</code></pre>

      <h2>Module: S3 Data Lake</h2>
      <p>A production-grade S3 data lake with proper lifecycle policies, encryption, and access controls:</p>
      <pre><code># modules/s3/main.tf
resource "aws_s3_bucket" "data_lake" {
  bucket = var.bucket_name
  
  tags = merge(var.common_tags, {
    DataClassification = var.classification
    Environment       = var.environment
  })
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  rule {
    id     = "transition-to-ia"
    status = "Enabled"
    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 365
      storage_class = "GLACIER"
    }
    expiration {
      days = 2555  # 7 years retention
    }
  }
  
  rule {
    id     = "cleanup-incomplete-uploads"
    status = "Enabled"
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}</code></pre>

      <h2>Managing State at Scale</h2>
      <p>For enterprise data platforms with multiple teams, proper state management is critical:</p>
      <pre><code># Backend configuration for remote state
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "data-platform/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
    kms_key_id     = "alias/terraform-state"
  }
}

# State isolation per environment
# Use workspaces or separate state files
locals {
  state_key = "\${var.environment}/terraform.tfstate"
}</code></pre>

      <h2>CI/CD Integration</h2>
      <p>Automate Terraform workflows with GitHub Actions for plan, review, and apply:</p>
      <pre><code># .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: ['terraform/**']
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.7.0"
      
      - name: Terraform Init
        run: terraform init
        working-directory: terraform/environments/prod
      
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: terraform/environments/prod
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
        working-directory: terraform/environments/prod</code></pre>

      <h2>Conclusion</h2>
      <p>Infrastructure as Code is not optional for modern data platforms. It's essential. Terraform provides the tooling, ecosystem, and patterns to manage complex data infrastructure at scale. By investing in modular, well-tested Terraform code, you gain the ability to spin up entire data platforms in minutes, replicate environments for testing, and maintain compliance through auditable infrastructure changes.</p>
    `
  },

  'real-time-feature-store': {
    title: 'Building a Real-Time Feature Store for Machine Learning',
    date: 'June 5, 2026',
    publishedAt: new Date('2026-06-05').getTime(),
    readTime: 17,
    tags: ['Feature Store', 'Machine Learning', 'Real-Time', 'Kafka', 'Redis'],
    category: 'Architecture',
    isDraft: false,
    featured: true,
    trending: true,
    excerpt: 'Learn how to design and implement a real-time feature store that bridges the gap between data engineering and machine learning teams. This comprehensive guide covers the architecture of feature stores including offline stores for batch feature computation, online stores for low-latency feature serving, and the streaming pipelines that keep them synchronized. Implement feature transformations using Apache Spark and Flink, store features in Redis and DynamoDB for sub-millisecond serving, and maintain feature freshness with Kafka streaming pipelines. Covers feature versioning, point-in-time correctness to prevent training-serving skew, feature monitoring and drift detection, and integration with ML frameworks like XGBoost, PyTorch, and scikit-learn. Includes architecture diagrams and code from a production feature store serving 50 million feature requests per day.',
    views: 3100,
    likes: 228,
    shares: 88,
    comments: 35,
    image: 'assets/images/real-time-analytics.png',
    content: `
      <h2>The Feature Store Problem</h2>
      <p>In production ML systems, the hardest part isn't training the model. It's serving features consistently between training and inference. When your training pipeline computes features differently than your serving system, you get <strong>training-serving skew</strong>, which silently degrades model performance. A <strong>feature store</strong> solves this by providing a shared, versioned layer for feature computation and serving.</p>

      <h2>Architecture Overview</h2>
      <p>A production feature store consists of three core components:</p>
      <ul>
        <li><strong>Offline Store:</strong> Batch-computed features in a data warehouse (Snowflake, BigQuery) for training.</li>
        <li><strong>Online Store:</strong> Low-latency feature serving from a key-value store (Redis, DynamoDB) for real-time inference.</li>
        <li><strong>Feature Pipeline:</strong> Streaming and batch pipelines that compute, transform, and synchronize features.</li>
      </ul>

      <h2>Feature Definitions</h2>
      <p>Define features declaratively with metadata, transformation logic, and serving requirements:</p>
      <pre><code># feature_definitions/user_features.py
from feature_store import Feature, Entity, FeatureGroup

# Define entities (the "keys" for feature lookup)
user_entity = Entity(
    name="user_id",
    description="Unique user identifier",
    dtype="string"
)

# Define feature group
user_features = FeatureGroup(
    name="user_behavioral_features",
    entity=user_entity,
    owner="ml-engineering",
    description="User behavioral features for churn prediction",
    freshness_policy={"max_age": "1h", "schedule": "*/15 * * * *"},
    online_store="redis",
    offline_store="snowflake",
    tags=["churn", "user-profile", "production"]
)

# Feature definitions
features = [
    Feature(
        name="user_avg_session_duration_7d",
        description="Average session duration over last 7 days",
        dtype="float64",
        transform="AVG(session_duration_seconds)",
        window="7d",
        aggregation="mean"
    ),
    Feature(
        name="user_total_purchases_30d",
        description="Total purchase count in last 30 days",
        dtype="int64",
        transform="COUNT(purchase_id)",
        window="30d",
        aggregation="count"
    ),
    Feature(
        name="user_last_login_days_ago",
        description="Days since last login",
        dtype="float64",
        transform="DATEDIFF(day, MAX(login_timestamp), CURRENT_DATE())",
        window="unbounded",
        aggregation="max"
    ),
    Feature(
        name="user_lifetime_value",
        description="Total revenue from user",
        dtype="float64",
        transform="SUM(purchase_amount)",
        window="unbounded",
        aggregation="sum"
    )
]</code></pre>

      <h2>Streaming Feature Pipeline with Flink</h2>
      <p>For real-time features, use Apache Flink to compute sliding window aggregations from Kafka streams:</p>
      <pre><code>// Flink streaming feature computation
DataStream<Event> events = env
    .addSource(new FlinkKafkaConsumer<>("user-events", 
        new EventSchema(), kafkaProps))
    .assignTimestampsAndWatermarks(
        WatermarkStrategy
            .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
            .withTimestampAssigner((e, t) -> e.getTimestamp())
    );

// Sliding window feature computation
DataStream<UserFeature> sessionFeatures = events
    .keyBy(Event::getUserId)
    .window(SlidingEventTimeWindows.of(
        Time.hours(24), Time.minutes(15)))
    .process(new SessionDurationProcessor());

// Write to Redis online store
sessionFeatures.addSink(new RedisSink<>(
    redisConfig,
    new UserFeatureRedisMapper()
));

// Write to S3 offline store (Parquet)
sessionFeatures
    .map(f -> f.toParquetRow())
    .addSink(new ParquetSink<>(s3Config));</code></pre>

      <h2>Online Feature Serving</h2>
      <p>Serve features with sub-millisecond latency for real-time inference:</p>
      <pre><code>import redis
import json
from typing import Dict, List

class FeatureStore:
    def __init__(self, redis_host: str, redis_port: int):
        self.redis = redis.Redis(
            host=redis_host, 
            port=redis_port,
            decode_responses=True
        )
    
    def get_online_features(
        self, 
        entity_id: str, 
        feature_names: List[str]
    ) -> Dict[str, float]:
        """Fetch features from online store with fallback."""
        pipe = self.redis.pipeline()
        
        for feature in feature_names:
            pipe.hget(f"features:{entity_id}", feature)
        
        results = pipe.execute()
        
        features = {}
        for name, value in zip(feature_names, results):
            if value is not None:
                features[name] = float(value)
            else:
                # Fallback to default or stale value
                features[name] = self._get_fallback(
                    entity_id, name
                )
        
        return features
    
    def get_historical_features(
        self,
        entity_ids: List[str],
        feature_names: List[str],
        point_in_time: str
    ) -> "DataFrame":
        """Fetch features for training with point-in-time correctness."""
        # Query Snowflake with time-travel to prevent leakage
        query = f"""
            SELECT entity_id, {', '.join(feature_names)}
            FROM feature_store.offline_features
            WHERE entity_id IN ({','.join(f"'{e}'" for e in entity_ids)})
            AND computed_at <= '{point_in_time}'
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY entity_id ORDER BY computed_at DESC
            ) = 1
        """
        return self._query_snowflake(query)</code></pre>

      <h2>Feature Monitoring</h2>
      <p>Monitor feature quality and drift to catch data issues before they impact model performance:</p>
      <ul>
        <li><strong>Freshness Monitoring:</strong> Alert when features haven't been updated within their expected freshness window.</li>
        <li><strong>Distribution Drift:</strong> Compare current feature distributions against training baselines using KS tests.</li>
        <li><strong>Null Rate Tracking:</strong> Monitor null percentages and alert when they exceed thresholds.</li>
        <li><strong>Feature Importance Changes:</strong> Track SHAP values over time to detect concept drift.</li>
      </ul>

      <h2>Conclusion</h2>
      <p>A well-designed feature store is the backbone of production ML systems. It ensures consistency between training and serving, reduces feature engineering duplication across teams, and provides the monitoring and governance needed for reliable model deployments. Start with clear feature definitions, build reliable streaming pipelines, and invest in monitoring from day one.</p>
    `
  },

  'data-observability-lineage': {
    title: 'The Complete Guide to Data Observability and Lineage Tracking',
    date: 'June 4, 2026',
    publishedAt: new Date('2026-06-04').getTime(),
    readTime: 15,
    tags: ['Data Observability', 'Data Lineage', 'Data Quality', 'Monitoring', 'Pipelines'],
    category: 'Data Quality',
    isDraft: false,
    featured: false,
    trending: true,
    excerpt: 'A comprehensive guide to building data observability into your organization. Monitoring data freshness, volume, schema changes, and quality across your entire pipeline. Learn how to implement automated data lineage tracking that maps dependencies from source to dashboard, set up anomaly detection for proactive alerting on data issues before they impact stakeholders, and build a data quality scorecard for organizational visibility. Covers open-source tools like OpenLineage, Marquez, and Elementary, as well as commercial platforms like Monte Carlo and Bigeye. Includes practical implementations of freshness checks, volume monitors, schema change detectors, and custom data contracts that prevent bad data from reaching downstream consumers. Real-world examples from monitoring 500+ tables across 20 data pipelines.',
    views: 2650,
    likes: 195,
    shares: 76,
    comments: 29,
    image: 'assets/images/data-quality-frameworks.png',
    content: `
      <h2>What is Data Observability?</h2>
      <p>Software engineering has long relied on observability, logs, metrics, and traces, to understand system behavior and debug issues. Data engineering needs the same rigor. <strong>Data observability</strong> is the practice of monitoring your data pipelines and datasets to detect, diagnose, and resolve data quality issues before they impact business decisions.</p>
      <p>The five pillars of data observability mirror the concept from software engineering:</p>
      <ul>
        <li><strong>Freshness:</strong> Is your data up to date? When was the last update?</li>
        <li><strong>Volume:</strong> Are you receiving the expected amount of data?</li>
        <li><strong>Schema:</strong> Has the structure of your data changed unexpectedly?</li>
        <li><strong>Distribution:</strong> Are the values within expected ranges?</li>
        <li><strong>Lineage:</strong> What depends on this data, and where does it come from?</li>
      </ul>

      <h2>Implementing Freshness Monitoring</h2>
      <p>The most common data incident is stale data. Set up automated freshness checks:</p>
      <pre><code># freshness_monitor.py
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class FreshnessCheck:
    table_name: str
    timestamp_column: str
    max_age_minutes: int
    alert_channels: list
    owner: str

class FreshnessMonitor:
    def __init__(self, db_connection, alert_fn: Callable):
        self.conn = db_connection
        self.alert_fn = alert_fn
    
    def check_table_freshness(self, check: FreshnessCheck) -> dict:
        """Check if a table's data is within the expected freshness window."""
        query = f"""
            SELECT 
                MAX({check.timestamp_column}) as last_update,
                COUNT(*) as total_rows,
                TIMESTAMPDIFF(MINUTE, 
                    MAX({check.timestamp_column}), 
                    CURRENT_TIMESTAMP()) as minutes_since_update
            FROM {check.table_name}
        """
        cursor = self.conn.execute(query)
        row = cursor.fetchone()
        
        result = {
            "table": check.table_name,
            "last_update": row[0],
            "total_rows": row[1],
            "minutes_since_update": row[2],
            "is_fresh": row[2] <= check.max_age_minutes,
            "severity": self._calculate_severity(row[2], check.max_age_minutes)
        }
        
        if not result["is_fresh"]:
            self.alert_fn(
                severity=result["severity"],
                message=f"Table {check.table_name} is stale. "
                        f"Last update: {row[2]} minutes ago "
                        f"(max: {check.max_age_minutes})",
                channels=check.alert_channels,
                owner=check.owner
            )
        
        return result
    
    def _calculate_severity(self, minutes_since: int, max_minutes: int) -> str:
        ratio = minutes_since / max_minutes
        if ratio <= 1.5: return "warning"
        if ratio <= 3.0: return "critical"
        return "emergency"</code></pre>

      <h2>Schema Change Detection</h2>
      <p>Unexpected schema changes break downstream queries silently. Detect them proactively:</p>
      <pre><code># schema_monitor.py
from typing import Dict, Set, List
import hashlib

class SchemaMonitor:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.schema_registry = {}
    
    def capture_schema(self, table_name: str) -> Dict[str, str]:
        """Capture current schema of a table."""
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """
        cursor = self.conn.execute(query)
        schema = {}
        for row in cursor.fetchall():
            schema[row[0]] = {
                "type": row[1],
                "nullable": row[2] == "YES"
            }
        return schema
    
    def detect_changes(self, table_name: str) -> List[dict]:
        """Compare current schema against baseline."""
        current = self.capture_schema(table_name)
        baseline = self.schema_registry.get(table_name, {})
        
        changes = []
        
        # Detect new columns
        new_cols = set(current.keys()) - set(baseline.keys())
        for col in new_cols:
            changes.append({
                "type": "column_added",
                "column": col,
                "details": current[col],
                "severity": "info"
            })
        
        # Detect removed columns
        removed_cols = set(baseline.keys()) - set(current.keys())
        for col in removed_cols:
            changes.append({
                "type": "column_removed",
                "column": col,
                "details": baseline[col],
                "severity": "critical"  # Breaking change!
            })
        
        # Detect type changes
        for col in set(current.keys()) & set(baseline.keys()):
            if current[col]["type"] != baseline[col]["type"]:
                changes.append({
                    "type": "type_changed",
                    "column": col,
                    "from": baseline[col]["type"],
                    "to": current[col]["type"],
                    "severity": "critical"
                })
        
        # Update baseline
        self.schema_registry[table_name] = current
        return changes</code></pre>

      <h2>Data Lineage with OpenLineage</h2>
      <p>OpenLineage provides an open standard for tracking data lineage across tools and platforms:</p>
      <pre><code># lineage_tracker.py
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, RunState
from openlineage.client.job import Job
import uuid

class LineageTracker:
    def __init__(self, api_url: str):
        self.client = OpenLineageClient(api_url)
        self.run_id = str(uuid.uuid4())
    
    def track_job_start(self, job_name: str, inputs: list, outputs: list):
        """Track the start of a data processing job."""
        event = RunEvent(
            eventType=RunState.START,
            run=self._create_run(),
            job=Job(namespace="production", name=job_name),
            inputs=[self._create_dataset(d) for d in inputs],
            outputs=[self._create_dataset(d) for d in outputs]
        )
        self.client.emit(event)
    
    def track_job_complete(self, job_name: str, inputs: list, outputs: list):
        """Track job completion with row counts."""
        event = RunEvent(
            eventType=RunState.COMPLETE,
            run=self._create_run(),
            job=Job(namespace="production", name=job_name),
            inputs=[self._create_dataset(d) for d in inputs],
            outputs=[self._create_dataset(d, rows=10000) for d in outputs]
        )
        self.client.emit(event)
    
    def _create_dataset(self, dataset_info: dict, rows: int = 0):
        from openlineage.client.dataset import Dataset
        return Dataset(
            namespace=dataset_info.get("namespace", "s3://data-lake"),
            name=dataset_info["name"],
            schema=None,
            description=None
        )
    
    def _create_run(self):
        from openlineage.client.run import Run
        return Run(runId=self.run_id)</code></pre>

      <h2>Building a Data Quality Scorecard</h2>
      <p>Create organizational visibility with a data quality scorecard:</p>
      <pre><code># Build a quality scorecard across all monitored tables
quality_scorecard = {
    "overall_score": 94.2,
    "freshness": {
        "score": 97.5,
        "tables_passing": 185,
        "tables_failing": 5,
        "critical_stale": 1
    },
    "volume": {
        "score": 92.1,
        "tables_passing": 178,
        "tables_failing": 12,
        "anomalies_detected": 8
    },
    "schema": {
        "score": 99.8,
        "tables_stable": 190,
        "recent_changes": 2,
        "breaking_changes": 0
    },
    "distribution": {
        "score": 87.3,
        "tables_normal": 170,
        "tables_drifting": 20,
        "critical_drift": 3
    }
}</code></pre>

      <h2>Conclusion</h2>
      <p>Data observability is not a luxury. It's a necessity for any organization that makes decisions based on data. By implementing monitoring across freshness, volume, schema, distribution, and lineage, you transform data quality from a reactive firefighting exercise into a proactive, measurable practice. Start with the basics (freshness and volume), add schema monitoring, and progressively build toward full lineage tracking. The investment pays for itself the first time it prevents a bad data incident from reaching your executives' dashboards.</p>
    `
  }
};
