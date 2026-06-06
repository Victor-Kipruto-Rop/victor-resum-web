/**
 * Posts Data Management
 * Central repository for all blog posts with metadata for search, filtering, and RSS feed generation
 * Structure: { postId: { title, date, readTime, excerpt, content, tags, isDraft } }
 */

window.posts = {
  'first-post': {
    title: 'Welcome to My Technical Blog',
    date: 'June 5, 2026',
    readTime: 5,
    tags: ['Introduction', 'Data Engineering', 'Career'],
    isDraft: false,
    excerpt: 'An introduction to my technical blog where I share insights on data engineering, ETL pipelines, and real-time systems.',
    content: `
      <p>Welcome to my technical blog! I'm Victor Kipruto Rop, a Data Engineer passionate about building scalable, production-grade data systems. This space is dedicated to sharing deep dives into the technologies and practices that power modern data infrastructure.</p>
      
      <h2>Why This Blog?</h2>
      <p>Throughout my journey as a data engineer, I've learned countless lessons from building ETL pipelines, streaming architectures, and data warehouses. Whether it's orchestrating complex DAGs with Apache Airflow, designing high-throughput Kafka consumers, or optimizing dimensional models in Snowflake, I've encountered challenges that I believe are worth documenting.</p>
      
      <p>This blog serves as both a knowledge repository and a platform to engage with the data engineering community. Each article dives into real-world problems and proven solutions.</p>
      
      <h2>What to Expect</h2>
      <p>Articles on this blog cover:</p>
      <ul>
        <li><strong>ETL & Orchestration</strong> — Apache Airflow, DAG design, error handling, monitoring</li>
        <li><strong>Stream Processing</strong> — Kafka architecture, producer/consumer patterns, real-time analytics</li>
        <li><strong>Data Warehousing</strong> — Dimensional modeling, Star Schema, SCD strategies, query optimization</li>
        <li><strong>DevOps & Infrastructure</strong> — Docker, CI/CD, cloud deployment, containerization best practices</li>
        <li><strong>Python & SQL</strong> — Code patterns, performance optimization, testing strategies</li>
      </ul>
      
      <h2>A Bit About Me</h2>
      <p>I'm a final-year BSc Data Science student at The Cooperative University of Kenya, specializing in data engineering for the past year. My practical experience includes building production systems that process millions of transactions daily (hello MPESA data!), designing resilient ETL pipelines, and contributing to cloud data infrastructure.</p>
      
      <p>Beyond the code, I'm a strong believer in continuous learning and mentorship. I love exploring new technologies, contributing to open-source, and collaborating with talented engineers.</p>
      
      <h2>Stay Connected</h2>
      <p>New articles are published regularly. Follow my GitHub for project updates, check out my portfolio for live examples, and don't hesitate to reach out via email or LinkedIn if you want to discuss data engineering, collaborate on projects, or just chat about technology.</p>
      
      <p>Let's build amazing data systems together! 🚀</p>
    `
  },
  
  'data-engineering': {
    title: 'Data Engineering Fundamentals: Building Scalable Systems from the Ground Up',
    date: 'June 4, 2026',
    readTime: 12,
    tags: ['Data Engineering', 'Architecture', 'Best Practices'],
    isDraft: false,
    excerpt: 'A comprehensive guide to data engineering fundamentals, covering architecture principles, ETL design patterns, and best practices for building production-grade data systems.',
    content: `
      <p>Data engineering is the backbone of modern data-driven organizations. While data science captures the headlines, it's data engineers who build the infrastructure that makes insights possible. In this article, we'll explore the fundamental principles of data engineering and the patterns that successful systems follow.</p>
      
      <h2>The Data Engineering Lifecycle</h2>
      <p>Every data system goes through distinct phases:</p>
      
      <h3>1. Data Ingestion</h3>
      <p>The first step is getting data into your system. Sources range from APIs and databases to message brokers and log streams. Key considerations:</p>
      <ul>
        <li><strong>Volume:</strong> How much data arrives per unit time?</li>
        <li><strong>Velocity:</strong> Is it real-time, batch, or micro-batch?</li>
        <li><strong>Variety:</strong> What formats? (JSON, CSV, Avro, Parquet)</li>
        <li><strong>Veracity:</strong> How reliable is the source? What error handling is needed?</li>
      </ul>
      
      <p>In production systems, I typically use Apache Kafka for high-velocity streams and scheduled batch jobs for periodic data dumps. The key is separating concerns: ingest raw data first, validate and transform downstream.</p>
      
      <h3>2. Storage & Transformation</h3>
      <p>Raw data isn't immediately useful. We need to:</p>
      <ul>
        <li><strong>Standardize schemas</strong> — Enforce consistent data types and formats</li>
        <li><strong>Deduplicate</strong> — Remove duplicate records from the source</li>
        <li><strong>Enrich</strong> — Join with reference data, add context</li>
        <li><strong>Clean</strong> — Handle missing values, outliers, anomalies</li>
      </ul>
      
      <p>This is where Apache Airflow shines. Orchestrating complex multi-step transformations with dependency management and failure recovery is its bread and butter.</p>
      
      <h3>3. Data Warehouse & Analytics</h3>
      <p>Transformed data lands in a warehouse optimized for analytical queries. The dimensional modeling approach (Kimball) remains the gold standard:</p>
      <ul>
        <li><strong>Fact tables:</strong> Measurable events (transactions, clicks, orders)</li>
        <li><strong>Dimension tables:</strong> Context attributes (customers, products, dates)</li>
        <li><strong>Star Schema:</strong> Simple joins, excellent query performance</li>
      </ul>
      
      <p>Tools like Snowflake, BigQuery, and PostgreSQL excel at this layer with columnar storage and query optimization.</p>
      
      <h2>The Three Pillars of Data Engineering</h2>
      
      <h3>Reliability</h3>
      <p>Your data pipelines must run predictably. This means:</p>
      <ul>
        <li>Idempotent operations (re-running produces same result)</li>
        <li>Comprehensive error handling and alerting</li>
        <li>Data quality checks at each stage</li>
        <li>Disaster recovery plans</li>
      </ul>
      
      <p>In Airflow, I use task dependencies and SLA callbacks. Failed tasks trigger alerts, and backfill operations let us recover from data gaps.</p>
      
      <h3>Scalability</h3>
      <p>Systems must handle 10x growth without major rewrites. Architecture decisions matter:</p>
      <ul>
        <li>Partition large tables by date/region for faster queries</li>
        <li>Use distributed processing (Spark, Kafka) for large datasets</li>
        <li>Implement connection pooling to avoid database bottlenecks</li>
        <li>Monitor resource usage and optimize hot paths</li>
      </ul>
      
      <h3>Maintainability</h3>
      <p>Code that isn't maintainable is a liability. Follow these practices:</p>
      <ul>
        <li>Modular DAGs with reusable operators</li>
        <li>Comprehensive logging and monitoring</li>
        <li>Clear documentation and runbooks</li>
        <li>Version control and CI/CD pipelines</li>
      </ul>
      
      <h2>Real-World Example: MPESA Transaction Pipeline</h2>
      <p>Let me share a practical example from my work. We built a high-throughput ingestion system for MPESA transaction data (think millions of daily transactions).</p>
      
      <p><strong>Architecture:</strong></p>
      <ul>
        <li>API → Python script with chunked reads and deduplication</li>
        <li>PostgreSQL staging tables with connection pooling</li>
        <li>Daily Airflow DAG that validates, transforms, and loads to warehouse</li>
        <li>Real-time Kafka stream for anomaly detection</li>
      </ul>
      
      <p><strong>Key learnings:</strong></p>
      <ul>
        <li>Chunked reads prevent memory overflows with large result sets</li>
        <li>Connection pooling reduces database overhead by 70%</li>
        <li>Deduplication on ingest prevents cascade errors downstream</li>
        <li>Separation of batch and real-time paths provides flexibility</li>
      </ul>
      
      <h2>Common Mistakes to Avoid</h2>
      <ul>
        <li><strong>Over-engineering:</strong> Start simple. Add complexity only when needed.</li>
        <li><strong>Ignoring data quality:</strong> Garbage in, garbage out. Validate early and often.</li>
        <li><strong>Tight coupling:</strong> Decouple components. Changes shouldn't cascade.</li>
        <li><strong>No monitoring:</strong> You can't fix what you can't see. Instrument everything.</li>
        <li><strong>Skipping documentation:</strong> Future you (or your colleague) will thank you.</li>
      </ul>
      
      <h2>The Road Ahead</h2>
      <p>Data engineering is evolving rapidly. Emerging trends include:</p>
      <ul>
        <li><strong>Data mesh:</strong> Decentralized data ownership and architecture</li>
        <li><strong>dbt revolution:</strong> SQL-first transformations with version control</li>
        <li><strong>Real-time everything:</strong> Moving beyond daily batch jobs</li>
        <li><strong>Data observability:</strong> Treating data quality as a first-class concern</li>
      </ul>
      
      <p>Whatever the future holds, the fundamentals remain: reliable systems, scalable architecture, and maintainable code.</p>
      
      <h2>Conclusion</h2>
      <p>Data engineering is both art and science. It requires understanding business context, technical depth in distributed systems, and the pragmatism to know when to accept imperfection. If you're starting your data engineering journey, focus on mastering these fundamentals before chasing every new tool.</p>
      
      <p>Questions? Thoughts? Reach out on LinkedIn or GitHub. I'm always excited to discuss data architecture!</p>
    `
  },

  'airflow-advanced': {
    title: 'Advanced Airflow Patterns & Optimization',
    date: 'May 28, 2026',
    readTime: 14,
    tags: ['Apache Airflow', 'Orchestration', 'Advanced'],
    isDraft: true,
    excerpt: 'Deep dive into dynamic DAG generation, custom operators, monitoring strategies, and scaling Airflow to handle thousands of concurrent tasks in production environments.',
    content: `
      <p>As your data infrastructure matures, basic Airflow DAGs become insufficient. You need patterns that enable scaling to thousands of tasks, dynamic pipeline generation, and advanced monitoring. This article explores production-grade techniques.</p>
      
      <h2>Dynamic DAG Generation</h2>
      <p>Instead of hardcoding task dependencies, generate them dynamically from configuration files or databases. This allows running hundreds of similar pipelines with a single DAG definition.</p>
      
      <h2>Custom Operators & Sensors</h2>
      <p>Built-in operators cover 80% of use cases. For the remaining 20%, custom operators provide type safety, reusability, and easier testing with pytest.</p>
      
      <h2>Performance Optimization</h2>
      <p>Techniques like connection pooling, batch processing, and distributed execution can reduce DAG execution time by 60-80%.</p>
    `
  },

  'kafka-streaming': {
    title: 'Real-time Event Streaming with Kafka and Python',
    date: 'May 15, 2026',
    readTime: 11,
    tags: ['Kafka', 'Streaming', 'Python'],
    isDraft: true,
    excerpt: 'Building high-throughput event streaming applications using Apache Kafka with Python producers and consumers, including error handling, exactly-once semantics, and performance tuning.',
    content: `
      <p>Kafka has become synonymous with real-time data pipelines. Building robust Kafka applications requires understanding its architecture, partitioning strategies, and consumer group coordination.</p>
      
      <h2>Producer Architecture</h2>
      <p>Producers can operate in fire-and-forget, synchronous, or asynchronous modes. Understanding trade-offs between throughput and durability is critical.</p>
      
      <h2>Consumer Coordination</h2>
      <p>Consumer groups enable horizontal scaling. However, managing offsets, rebalancing, and failure recovery requires careful implementation.</p>
      
      <h2>Building a Real-time Dashboard</h2>
      <p>Combine Kafka with WebSockets to build live dashboards that update as events arrive, creating a truly reactive data experience.</p>
    `
  },

  'dbt-fundamentals': {
    title: 'dbt (Data Build Tool): SQL-First Data Transformation',
    date: 'April 30, 2026',
    readTime: 9,
    tags: ['dbt', 'SQL', 'Transformation'],
    isDraft: true,
    excerpt: 'Getting started with dbt for version-controlled, tested SQL transformations. Learn models, tests, documentation, and how dbt revolutionizes the modern data stack.',
    content: `
      <p>dbt has fundamentally changed how data teams approach transformations. By combining SQL with software engineering practices, dbt brings structure, testability, and version control to data work.</p>
      
      <h2>Models as Abstraction</h2>
      <p>dbt models are SQL SELECT statements wrapped with metadata. They enable reusability, clarity, and dependency management.</p>
      
      <h2>Testing & Documentation</h2>
      <p>Built-in testing frameworks catch data quality issues before they impact analytics. Auto-generated documentation keeps your warehouse self-documenting.</p>
      
      <h2>Macro Magic</h2>
      <p>Advanced dbt users leverage macros (Jinja2 templates) to DRY up SQL, create custom macros, and build reusable transformation logic.</p>
    `
  },

  'snowflake-performance': {
    title: 'Snowflake Query Optimization & Cost Management',
    date: 'April 12, 2026',
    readTime: 10,
    tags: ['Snowflake', 'Performance', 'Cost Optimization'],
    isDraft: true,
    excerpt: 'Techniques for optimizing Snowflake queries, reducing compute costs, and leveraging features like materialized views and clustering for better performance.',
    content: `
      <p>Snowflake\'s pay-as-you-go model makes cost optimization critical. A poorly written query can cost hundreds of dollars. This guide covers optimization strategies at every level.</p>
      
      <h2>Query Planning</h2>
      <p>Understanding EXPLAIN plans is fundamental. Learn to identify full table scans, expensive joins, and other performance killers.</p>
      
      <h2>Materialized Views</h2>
      <p>Materialized views cache query results for reuse. For analytical queries run repeatedly, they can provide 10x speedups at fraction of the cost.</p>
      
      <h2>Warehouse Sizing</h2>
      <p>Right-sizing warehouses balances speed and cost. Larger warehouses run queries faster but cost more per second.</p>
    `
  }
};
