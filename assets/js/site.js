/* Shared site script — extracted from index.html / projects/index.html / contact/index.html (previously ~70KB of near-identical inline <script> blocks duplicated on every page load). Loaded at the end of <body>, after all the DOM elements it references, so document.getElementById() calls resolve correctly. */

function openCvModal() {
    document.getElementById('cvModalOverlay').style.display = 'flex';
  }
  function closeCvModal() {
    document.getElementById('cvModalOverlay').style.display = 'none';
    document.getElementById('cvSuccessMsg').style.display = 'none';
  }
  function downloadCv() {
    const link = document.createElement('a');
    link.href = 'assets/Victor_Kipruto_Resume.pdf';
    link.download = 'Victor_Kipruto_Resume.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    document.getElementById('cvSuccessMsg').style.display = 'block';
    setTimeout(closeCvModal, 2000);
  }

  function openCertModal(url) {
    const overlay = document.getElementById('certModalOverlay');
    const iframe = document.getElementById('certModalIframe');
    iframe.src = url;
    overlay.style.display = 'flex';
  }
  function closeCertModal() {
    const overlay = document.getElementById('certModalOverlay');
    const iframe = document.getElementById('certModalIframe');
    iframe.src = '';
    overlay.style.display = 'none';
  }

const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;
  
  // Check for saved theme - fall back to system preference, then dark mode
  const savedTheme = localStorage.getItem('theme');
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  if (savedTheme === 'light' || (!savedTheme && prefersLight)) {
    body.classList.remove('dark-mode');
  } else {
    body.classList.add('dark-mode');
  }

  themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const theme = body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
  });

  // Pre-loader and Page Entrance
  window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    const heroName = document.getElementById('hero-name');
    
    // Split hero name into characters for staggered reveal
    if (heroName) {
      const text = heroName.textContent;
      heroName.innerHTML = text.split('').map((char, i) => 
        `<span style="display:inline-block; animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards ${0.5 + i * 0.03}s; transform: translateY(100%); opacity: 0;">${char === ' ' ? '&nbsp;' : char}</span>`
      ).join('');
      // Apply fadeUp to children manually since we replaced innerHTML
      Array.from(heroName.children).forEach(span => {
        span.style.opacity = '1'; 
      });
    }

    setTimeout(() => {
      preloader.classList.add('hidden');
      document.body.classList.add('loaded');
    }, 1000);
  });

  // Magnetic Buttons
  const magneticBtns = document.querySelectorAll('.magnetic');
  magneticBtns.forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      btn.style.transform = `translate(${x * 0.3}px, ${y * 0.5}px)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0, 0)';
    });
  });

  // 3D Tilt for Cards
  function applyTilt(elements) {
    elements.forEach(el => {
      el.addEventListener('mousemove', e => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
      });
      el.addEventListener('mouseleave', () => {
        el.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
      });
    });
  }
  // Apply initially to "Why Hire Me" cards
  applyTilt(document.querySelectorAll('.why-card'));
  applyTilt(document.querySelectorAll('.experience-card'));
  applyTilt(document.querySelectorAll('.cert-card'));

  // Cursor
  const cur = document.getElementById('cursor');
  const ring = document.getElementById('cursor-ring');
  document.addEventListener('mousemove', e => {
    cur.style.transform  = `translate(${e.clientX - 5}px, ${e.clientY - 5}px)`;
    ring.style.transform = `translate(${e.clientX - 18}px, ${e.clientY - 18}px)`;
  });

  // Scroll reveal
  window.obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => window.obs.observe(el));

  // Nav scroll-spy: highlight the active section link with a sliding underline
  (function () {
    const navAnchorLinks = Array.from(document.querySelectorAll('.nav-links a[href^="#"]'));
    if (!navAnchorLinks.length) return;
    const idToLink = new Map(navAnchorLinks.map(a => [a.getAttribute('href').slice(1), a]));
    const spy = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const link = idToLink.get(entry.target.id);
          if (link) {
            navAnchorLinks.forEach(a => a.classList.remove('active-link'));
            link.classList.add('active-link');
          }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    idToLink.forEach((link, id) => {
      const el = document.getElementById(id);
      if (el) spy.observe(el);
    });
  })();


  // Projects horizontal scroll helper
  const projectsGrid = document.getElementById('projects-grid');
  const prevBtn = document.querySelector('.project-prev');
  const nextBtn = document.querySelector('.project-next');
  function scrollProjects(dir){
    if(!projectsGrid) return;
    const card = projectsGrid.querySelector('.project-card');
    const cardWidth = card ? Math.round(card.getBoundingClientRect().width) : 320;
    const gap = 24;
    const offset = (cardWidth + gap) * 1 * dir; // scroll one card per click
    projectsGrid.scrollBy({ left: offset, behavior: 'smooth' });
  }
  // Arrow visibility updater
  function updateProjectArrows(){
    if(!projectsGrid || !prevBtn || !nextBtn) return;
    const isMobile = window.innerWidth <= 540;
    const left = Math.round(projectsGrid.scrollLeft);
    const max = projectsGrid.scrollWidth - projectsGrid.clientWidth;
    if(isMobile){ prevBtn.style.opacity='1'; nextBtn.style.opacity='1'; prevBtn.style.pointerEvents='auto'; nextBtn.style.pointerEvents='auto'; return; }
    if(left <= 8){ prevBtn.style.opacity='0'; prevBtn.style.pointerEvents='none'; } else { prevBtn.style.opacity='1'; prevBtn.style.pointerEvents='auto'; }
    if(left >= Math.round(max - 8)){ nextBtn.style.opacity='0'; nextBtn.style.pointerEvents='none'; } else { nextBtn.style.opacity='1'; nextBtn.style.pointerEvents='auto'; }
  }
  // Optional keyboard support
  document.addEventListener('keydown', (e) => {
    if(document.activeElement && ['INPUT','TEXTAREA','BUTTON'].includes(document.activeElement.tagName)) return;
    if(e.key === 'ArrowRight') scrollProjects(1);
    if(e.key === 'ArrowLeft') scrollProjects(-1);
  });
  if(projectsGrid){ projectsGrid.addEventListener('scroll', updateProjectArrows); }
  window.addEventListener('resize', updateProjectArrows);
  // initial arrows state
  updateProjectArrows();
  document.addEventListener('DOMContentLoaded', () => { setTimeout(updateProjectArrows, 120); });

  // Formspree error handling (Success is handled via redirect)
  const fsError = document.querySelector('[data-fs-error]');
  const contactForm = document.getElementById('contact-form');

  // Skills displayed as tag lists. No percentage fills. Skill-cards are already animated via the `.reveal` observer.

  // Fetch GitHub repos and render project cards dynamically
  function escapeHtml(str){ return str ? String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') : ''; }
  async function fetchRepos(){
    try{
      const res = await fetch('https://api.github.com/users/Victor-Kipruto-Rop/repos?per_page=100');
      if(!res.ok) throw new Error('GitHub API error');
      const repos = await res.json();
      // exclude personal/placeholder repos
      const deKeywords = ['data', 'engineer', 'etl', 'airflow', 'spark', 'sql', 'warehouse', 'pipeline', 'kafka', 'flink', 'dbt', 'bigquery', 'snowflake', 'analytics', 'streaming'];
      const filtered = (Array.isArray(repos) ? repos.filter(r => {
        if (!r || !r.name) return false;
        if (r.name.toLowerCase() === 'victor-kipruto-rop' || r.name.toLowerCase() === 'kipruto45') return false;
        const nameDesc = (r.name + ' ' + (r.description || '')).toLowerCase();
        const isMatch = deKeywords.some(keyword => nameDesc.includes(keyword));
        if (isMatch) console.log('Match found:', r.name);
        return isMatch;
      }) : []);

      console.log('Filtered projects count:', filtered.length);
      // sort by popularity (stars) then recent activity
      filtered.sort((a,b)=> {
        const starsA = a.stargazers_count || 0; const starsB = b.stargazers_count || 0;
        if(starsB !== starsA) return starsB - starsA;
        return new Date(b.pushed_at) - new Date(a.pushed_at);
      });

      // show all relevant projects
      const display = filtered;
      console.log('Displaying projects:', display.map(p => p.name));
      // Map specific repos to images
      const projectImageMap = {
        'Real_Time_Transaction_Streaming-MPESA-': 'assets/images/4.jpeg',
        'cloud-etl-pipeline': 'assets/images/2.jpeg',
        'Data-Enginerring-full-project': 'assets/images/1.jpeg',
        'mpesa_safaricom-pipeline-': 'assets/images/3.jpeg'
      };
      
      const grid = document.getElementById('projects-grid');
      if(!grid) return;
      grid.innerHTML = '';

      // fetch extra details per repo (topics, full description) and contents to infer tools
      const cards = await Promise.all(display.map(async (r, idx) => {
        let details = r;
        try{
          const dres = await fetch(r.url, { headers: { Accept: 'application/vnd.github.mercy-preview+json' } });
          if(dres.ok) details = await dres.json();
        }catch(e){ /* ignore */ }

        const topics = (details.topics && details.topics.length) ? details.topics : [];
        const language = details.language || r.language || '';

        const owner = r.owner && r.owner.login ? r.owner.login : 'Victor-Kipruto-Rop';
        const repoName = r.name;
        let contents = [];
        try{
          const cres = await fetch(`https://api.github.com/repos/${owner}/${repoName}/contents`);
          if(cres.ok) contents = await cres.json();
        }catch(e){ /* ignore */ }
        const fileNames = (Array.isArray(contents) ? contents.map(c=>c.name.toLowerCase()) : []);
        const dirNames = (Array.isArray(contents) ? contents.filter(c=>c.type==='dir').map(c=>c.name.toLowerCase()) : []);

        const found = new Set();
        if(fileNames.includes('dockerfile') || fileNames.some(n=>n.includes('dockerfile'))) found.add('Docker');
        if(fileNames.includes('docker-compose.yml') || fileNames.includes('docker-compose.yaml')) found.add('Docker Compose');
        if(fileNames.includes('requirements.txt') || fileNames.includes('pipfile') || fileNames.includes('pyproject.toml')) found.add('Python');
        if(fileNames.includes('package.json')) found.add('Node.js');
        if(fileNames.some(n=>n.endsWith('.ipynb'))) found.add('Jupyter');
        if(fileNames.some(n=>n.endsWith('.sql'))) found.add('SQL');
        if(fileNames.some(n=>n.includes('kafka'))) found.add('Kafka');
        if(fileNames.some(n=>n.endsWith('.tf')) || fileNames.some(n=>n.includes('terraform'))) found.add('Terraform');
        if(fileNames.some(n=>n.includes('spark')||n.includes('pyspark'))) found.add('Apache Spark');
        if(fileNames.some(n=>n.includes('snowflake'))) found.add('Snowflake');

        if(dirNames.includes('dags') || dirNames.includes('airflow')) found.add('Apache Airflow');
        if(dirNames.includes('notebooks') || dirNames.includes('nb')) found.add('Jupyter');
        if(dirNames.includes('.github')){
          try{
            const wres = await fetch(`https://api.github.com/repos/${owner}/${repoName}/contents/.github/workflows`);
            if(wres.ok){ const wf = await wres.json(); if(Array.isArray(wf) && wf.length) found.add('GitHub Actions'); }
          }catch(e){}
        }

        let readmeText = '';
        try{
          const rres = await fetch(`https://api.github.com/repos/${owner}/${repoName}/readme`);
          if(rres.ok){
            const rjson = await rres.json();
            if(rjson && rjson.content){
              try{ 
                readmeText = atob(rjson.content.replace(/\n/g,''));
                const ltxt = readmeText.toLowerCase();
                if(ltxt.includes('snowflake')) found.add('Snowflake');
                if(ltxt.includes('spark')) found.add('Apache Spark');
                if(ltxt.includes('airflow')) found.add('Apache Airflow');
                if(ltxt.includes('kafka')) found.add('Kafka');
                if(ltxt.includes('dbt')) found.add('dbt');
              }catch(e){}
            }
          }
        }catch(e){}

        const tools = [];
        found.forEach(t => tools.push(t));
        if(language && !tools.includes(language)) tools.push(language);
        topics.forEach(t => { if(!tools.includes(t)) tools.push(t); });
        if(!tools.length) tools.push(language || 'Repo');
        const toolsTrim = tools.slice(0,8);

        let desc = (details.description || r.description || '').trim();
        if(!desc && readmeText){
          const p = readmeText.split(/\n\n+/).find(s=>s.trim().length>20) || readmeText;
          desc = p.replace(/[#_*`>-]/g,'').trim().slice(0,260);
          if(desc.length === 260) desc += '...';
        }
        if(!desc) desc = `${r.name.replace(/[-_]/g,' ')}. ${toolsTrim.join(', ')}.`;

        const card = document.createElement('div');
        card.className = 'project-card reveal';
        card.style.transitionDelay = (idx * 0.08) + 's';
        
        // Use mapped image or fallback to a default image
        const thumb = projectImageMap[r.name] || 'assets/images/1.jpeg';
        
        const projectData = {
          title: r.name.replace(/[-_]/g, ' '),
          desc: desc,
          stack: toolsTrim,
          img: thumb,
          view: r.html_url
        };
        
        card.onclick = () => openProjectModal(projectData);
        
        card.innerHTML = `
          <img class="project-thumb" src="${thumb}" alt="${escapeHtml(r.name)}" loading="lazy" />
          <div class="project-content">
            <p class="project-title">${escapeHtml(r.name.replace(/[-_]/g, ' '))}</p>
            <p class="project-desc">${escapeHtml(desc)}</p>
            <div class="project-stack">
              ${toolsTrim.map(t => `<span class="stack-badge">${escapeHtml(t)}</span>`).join('')}
            </div>
            <div class="project-actions">
              <a class="btn-sm btn-primary-sm" href="${r.html_url}" target="_blank" rel="noopener" aria-label="View project ${escapeHtml(r.name)} on GitHub">View</a>
              <a class="btn-sm btn-outline" href="${r.html_url}/blob/main/README.md" target="_blank" rel="noopener" aria-label="Read documentation for ${escapeHtml(r.name)}">Readme</a>
            </div>
          </div>
        `;
        return card;
      }));

      cards.forEach(card => {
        grid.appendChild(card);
        if(window.obs) window.obs.observe(card);
      });
      applyTilt(cards);
      setTimeout(updateProjectArrows, 120);
    } catch(e) {
      console.error('fetchRepos failed', e);
      ensureStaticProjects();
    }
  }

  // Hamburger menu toggle
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      navLinks.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', hamburger.classList.contains('active'));
    });
    // Close menu when a link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });
  }
  

  // Call render for the curated case-study projects on load
  document.addEventListener('DOMContentLoaded', ()=>{ 
  ensureStaticProjects();
  });
  // ensure projects are visible: if projects-grid is empty, populate static fallback cards
  function ensureStaticProjects(){
    const grid = document.getElementById('projects-grid');
    if(!grid) return;
    if(grid.children.length > 0) return; // already populated
    const staticProjects = [
      { img: 'assets/images/2.jpeg', title: 'Cloud ETL Pipeline', desc: 'Processed 1.6M+ records at ~70,000 rows/sec with peak memory under 300MB via chunked reading and automatic encoding detection. Idempotent batch upserts and aggregation-based deduplication give the pipeline fault tolerance, cutting full load time from 4 minutes to 45 seconds.', stack: ['Python','Pandas','PostgreSQL','SQLAlchemy','Docker','Pytest','GitHub Actions'], view: 'https://github.com/Victor-Kipruto-Rop/cloud-etl-pipeline' },
      { img: 'assets/images/3.jpeg', title: 'M-Pesa Airflow Transaction Pipeline', desc: 'DAG-orchestrated M-Pesa transaction processing with a Faker-driven synthetic data generator, a rule-engine-based multi-stage cleaning pipeline, and a Docker Compose stack reproducible with a single command.', stack: ['Apache Airflow','Python','Faker','PostgreSQL','Docker Compose','Pytest','GitHub Actions'], view: 'https://github.com/Victor-Kipruto-Rop/mpesa_safaricom-pipeline-' },
      { img: 'assets/images/4.jpeg', title: 'Real-Time Transaction Streaming System', desc: 'Kafka producer/consumer model for live transaction ingestion, with consumer-group design for horizontal scalability and exactly-once semantics to prevent double-counting, plus live Plotly visualisations rendered from the consumer layer in Jupyter.', stack: ['Apache Kafka','Python','Jupyter','Plotly','Docker Compose','GitHub Actions'], view: 'https://github.com/Victor-Kipruto-Rop/Real_Time_Transaction_Streaming-MPESA-' },
      { img: 'assets/images/3.jpeg', title: 'End-to-End SQL Pipeline Portfolio', desc: 'Multi-tier data lake pattern from CSV staging through OLTP models into a star schema warehouse, with SCD Type 2 on customer dimensions and recursive CTE queries surfacing revenue shifts, fraud signals, and retention metrics.', stack: ['Python','PostgreSQL','AWS S3','SQLAlchemy','SCD Type 2'], view: '' },
      { img: 'assets/images/4.jpeg', title: 'Streaming Pipeline', desc: 'A real-time data streaming pipeline for scalable ingestion, processing, transformation, and analytics of continuous data streams.', stack: ['Python'], view: 'https://github.com/Victor-Kipruto-Rop/streaming-pipeline' },
      { img: 'assets/images/5.jpeg', title: 'Early Portfolio Site', desc: 'My first public portfolio project, built under an earlier GitHub handle before consolidating my work under this account.', stack: ['Python'], view: 'https://github.com/Victor-Kipruto-Rop/kipruto45-victor-kipruto-rop-portfolio' }
    ];
    grid.innerHTML = '';
    staticProjects.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = 'project-card reveal';
      card.style.transitionDelay = (idx*0.08)+'s';
      card.onclick = () => openProjectModal(p);
      const actions = p.view
        ? `<a class="btn-sm btn-primary-sm" href="${p.view}" target="_blank" rel="noopener" aria-label="View project ${p.title}">View</a>\n            <a class="btn-sm btn-outline" href="${p.view}" target="_blank" rel="noopener" aria-label="Read documentation for ${p.title}">Readme</a>`
        : `<span class="btn-sm btn-outline" style="cursor:default;">Private Repository · Live Pilot</span>`;
      card.innerHTML = `\n        <img class="project-thumb" src="${p.img}" alt="${p.title}" loading="lazy" />\n        <div class="project-content">\n          <p class="project-title">${p.title}</p>\n          <p class="project-desc">${p.desc}</p>\n          <div class="project-stack">${p.stack.map(s=>`<span class="stack-badge">${s}</span>`).join('')}</div>\n          <div class="project-actions">\n            ${actions}\n          </div>\n        </div>`;
      grid.appendChild(card);
      if(window.obs) window.obs.observe(card);
    });
    applyTilt(grid.querySelectorAll('.project-card'));
    setTimeout(updateProjectArrows, 120);
  }

  // Contact form integration (Formspree AJAX)
  window.formspree = window.formspree || function () { (formspree.q = formspree.q || []).push(arguments); };
  formspree('initForm', { 
    formElement: '#contact-form', 
    formId: 'xkoagvvk',
    onSuccess: (form, data) => {
      window.location.href = '/success';
    }
  });

// Analytics tracking
  const subscriptionAnalytics = {
    init() {
      const defaults = {
        rss_clicks: 0,
        inoreader_clicks: 0,
        feedly_clicks: 0,
        email_subscriptions: 0,
        telegram_subscriptions: 0,
        copy_clicks: 0
      };
      if (!localStorage.getItem('subscriptionAnalytics')) {
        localStorage.setItem('subscriptionAnalytics', JSON.stringify(defaults));
      }
    },
    track(event) {
      const analytics = JSON.parse(localStorage.getItem('subscriptionAnalytics') || '{}');
      if (analytics[event] !== undefined) {
        analytics[event]++;
        localStorage.setItem('subscriptionAnalytics', JSON.stringify(analytics));
      }
    },
    get(event) {
      const analytics = JSON.parse(localStorage.getItem('subscriptionAnalytics') || '{}');
      return analytics[event] || 0;
    },
    getAll() {
      return JSON.parse(localStorage.getItem('subscriptionAnalytics') || '{}');
    }
  };

  // Project Modal Management
  const projectExtendedData = {
    'PesaGuard': {
      time: '2026, Ongoing (Live Pilot)',
      category: 'FinTech Reconciliation & Fraud Detection',
      caseStudy: {
        problem: 'Kenyan SACCOs, e-commerce operators, and small fintechs receive M-Pesa payments through Safaricom\'s Daraja API but have no reliable way to reconcile incoming transactions against their own ledgers or catch anomalies in real time. Reconciliation is typically a manual, end-of-day spreadsheet exercise.',
        requirements: 'Real-time ingestion of Daraja webhook callbacks; guaranteed exactly-once processing (Safaricom retries webhooks, so duplicates are a certainty, not an edge case); an audit trail finance teams can trust; a system that degrades safely rather than silently losing a transaction.',
        architecture: 'Flask/Python backend, Next.js 14 frontend, PostgreSQL via Supabase, deployed on Render. A target-state Backend Software Architecture Specification (BSAS) was also produced, scoping the system out to enterprise scale (100M transactions/day), 12 subsystems and 10 frontend pages mapped end to end, so today\'s MVP decisions don\'t box in later growth.',
        dataFlow: 'Daraja sends a webhook → request hits the Flask ingestion endpoint → idempotency check against a processed-events store → reconciliation engine matches the transaction to expected records → result persisted to Postgres → surfaced on the Next.js dashboard.',
        techDecisions: 'Flask over a heavier framework for a lean MVP; Supabase Postgres over a self-managed database to remove ops overhead while validating product-market fit with the pilot customer; Render for zero-maintenance deployment at this stage. Deliberately framed as MVP-stage choices, with the BSAS defining where each would need to change at scale.',
        implementation: 'The core reconciliation engine matches incoming Daraja events against expected transaction records. Webhook idempotency was implemented via idempotency_keys and processed_events guards enforced across models.py, event_store.py, and reconciliation_engine.py, so a retried webhook can never be double-counted.',
        dataQuality: 'Every incoming webhook is checked against its idempotency key before it touches business logic, so retries and duplicate deliveries are filtered before they can corrupt a balance. Input validation on webhook payloads is the next hardening item in progress.',
        errorHandling: 'The idempotency layer is the first line of defense. A duplicate or malformed event is caught and logged rather than silently reprocessed. A traceable audit trail and verified backup/restore are treated as pre-launch requirements, not nice-to-haves.',
        performance: 'Not yet load-tested against production-scale volume. The current milestone is correctness with a single pilot customer, with the BSAS defining the path to 100M transactions/day once the fundamentals are proven.',
        observability: 'Alerting is on the hardening checklist with an explicit requirement that it be proven to fire end-to-end, not just configured and assumed to work.',
        security: 'A SECURITY.md policy is published on the related public repo; input validation and a full audit trail are treated as blocking requirements before new feature work.',
        results: 'Live with one pilot customer processing real M-Pesa transactions. Webhook idempotency, the highest-priority unshipped risk, has shipped and is verified across the reconciliation engine.',
        lessonsLearned: 'Planning had been outpacing implementation. A large body of architecture and roadmap documents existed before idempotency, the actual highest-risk gap, was closed. The lesson applied going forward: ship the boring, high-risk plumbing before new features, no matter how much design work already exists.'
      }
    },
    'Cloud ETL Pipeline': {
      time: 'Jan 2026 - Feb 2026',
      category: 'Infrastructure & Automation',
      caseStudy: {
        problem: 'Loading large CSV exports row-by-row into Postgres was slow enough to become a bottleneck, and a pipeline re-run after a partial failure risked producing duplicate or corrupted rows.',
        requirements: 'Handle over a million records without exhausting memory, guarantee that a failed or re-run job never corrupts state, and cut load time meaningfully without sacrificing correctness.',
        architecture: 'A Python pipeline using Pandas for transformation and SQLAlchemy for the PostgreSQL write layer, containerised with Docker.',
        dataFlow: 'Source files → chunked reading with automatic encoding detection → Pandas cleaning and deduplication → idempotent batch upserts into PostgreSQL.',
        techDecisions: 'Pandas for the transformation layer because vectorised operations made deduplication logic far simpler than row-by-row loops. Idempotent upserts, rather than plain inserts, specifically so a failed or re-run job can\'t corrupt state. That\'s what fault tolerance actually means in a batch pipeline like this. Docker so the pipeline runs identically in CI and production.',
        implementation: 'Deduplication is implemented as an aggregation step, conflicting records are merged by a defined rule rather than one being silently dropped, and the whole write path is idempotent so re-running the pipeline never double-counts a row.',
        dataQuality: 'Automatic encoding detection at the read stage catches malformed files before they reach the transform logic, and the deduplication/aggregation step prevents conflicting records from silently overwriting one another.',
        errorHandling: 'Idempotent batch upserts mean a failed job can simply be re-run from the start without manual cleanup or risk of duplicated data.',
        performance: 'Processed over 1.6 million records at roughly 70,000 rows/sec with peak memory held under 300MB, cutting full load time from 4 minutes to 45 seconds by moving from per-row inserts to batched execution with a tuned connection pool.',
        observability: 'CI-gated test runs on every push mean regressions in the transformation or deduplication logic are caught before merge, not after deployment.',
        security: 'Database credentials are handled through configuration rather than embedded in pipeline code.',
        results: 'A fault-tolerant, idempotent ETL pipeline processing 1.6M+ records at ~70,000 rows/sec with load time cut from 4 minutes to 45 seconds.',
        lessonsLearned: 'The real bottleneck wasn\'t reading or transforming the data. It was the insert pattern. Batching writes and making the pipeline idempotent had a far bigger impact on both reliability and speed than anything done to the read or transform stages.'
      }
    },
    'M-Pesa Airflow Transaction Pipeline': {
      time: 'Nov 2025 - Dec 2025',
      category: 'FinTech Data Systems',
      caseStudy: {
        problem: 'Testing an M-Pesa ingestion pipeline against real transaction data isn\'t practical or safe. It needs realistic-looking test data without ever touching actual customer records.',
        requirements: 'A synthetic data generator realistic enough to exercise real edge cases, a cleaning pipeline configurable without code changes, and a stack that runs identically for every contributor and in CI.',
        architecture: 'Airflow DAGs orchestrate a configurable synthetic data generator (Faker) into a multi-stage, config-driven cleaning pipeline, writing to PostgreSQL, all fully containerised via Docker Compose.',
        dataFlow: 'Faker generates synthetic M-Pesa-style transactions with realistic Kenyan phone number distributions → an Airflow DAG stages clean and validate the data → cleaned records land in PostgreSQL.',
        techDecisions: 'Faker over hand-written fixtures because realistic phone number and transaction distributions catch edge cases fixed test data wouldn\'t. A config-driven cleaning pipeline over hardcoded rules so cleaning logic can change without touching pipeline code. Docker Compose so the whole Airflow + PostgreSQL stack starts identically for any contributor or CI run.',
        implementation: 'The cleaning pipeline reads its rules from configuration, so stages like field normalisation and validation are driven by config files rather than being hardcoded into DAG tasks.',
        dataQuality: 'Multi-stage cleaning validates each transformation before the next stage runs, and the generated data\'s realistic phone number distributions mean tests exercise genuine edge cases.',
        errorHandling: 'Airflow\'s task-level retry and failure states apply to each cleaning stage independently, so one bad batch doesn\'t require rerunning the whole DAG.',
        performance: 'Containerised, reproducible runs mean performance characteristics stay consistent between a contributor\'s laptop and CI, not something that only shows up in production.',
        observability: 'Pytest coverage plus GitHub Actions CI mean pipeline correctness is checked automatically on every push, not just spot-checked manually.',
        security: 'Fully synthetic data means the pipeline can be developed, tested, and demoed without ever touching real customer transaction data.',
        results: 'A fully containerised, reproducible Airflow + PostgreSQL stack with config-driven cleaning and realistic synthetic test data.',
        lessonsLearned: 'Investing in a realistic synthetic data generator upfront paid off more than expected. Most of the genuinely interesting edge cases in the cleaning pipeline were found via Faker-generated data, not by staring at the code.'
      }
    },
    'Real-Time Transaction Streaming System': {
      time: 'Dec 2025 - Jan 2026',
      category: 'FinTech Streaming Architecture',
      caseStudy: {
        problem: 'A single consumer processing a transaction stream becomes a throughput ceiling, and without exactly-once guarantees, consumer restarts or rebalances risk double-counting transactions.',
        requirements: 'Horizontal scalability on the consumer side, exactly-once processing semantics, and low-latency real-time aggregation visible as it happens.',
        architecture: 'A Kafka producer/consumer model with consumer-group design, feeding real-time aggregation logic visualised live via Plotly inside Jupyter, running in a Docker Compose stack.',
        dataFlow: 'Producer publishes transaction events to a Kafka topic → a consumer group processes partitions in parallel → real-time aggregation logic updates running totals → Plotly renders live visualisations inside a Jupyter notebook.',
        techDecisions: 'Kafka\'s consumer-group model chosen specifically for horizontal scalability. Adding consumers increases throughput without redesigning the pipeline. Exactly-once semantics implemented deliberately rather than accepting at-least-once delivery, since double-counted transactions would corrupt aggregates. Jupyter + Plotly for visualisation because it made iterating on the aggregation logic and immediately seeing the result the fastest feedback loop.',
        implementation: 'Exactly-once semantics are enforced at the consumer level so a rebalance or restart can\'t cause a transaction to be counted twice in the aggregate.',
        dataQuality: 'Exactly-once processing is itself a data-quality guarantee. It\'s the difference between an aggregate you can trust and one that silently drifts upward every time a consumer restarts.',
        errorHandling: 'Consumer-group rebalancing is handled as a normal operational event, not a failure mode, since exactly-once semantics mean a rebalance can\'t corrupt in-flight aggregation state.',
        performance: 'Consumer-group parallelism is what actually delivers low-latency throughput at scale. A single consumer would cap throughput regardless of how optimised its processing logic was.',
        observability: 'Live Plotly visualisations inside Jupyter mean aggregation behaviour is visible in real time during development, not just inferred from logs after the fact.',
        security: 'Runs inside an isolated Docker Compose network, with topic-level access scoped to only the producer and consumer-group services that need it.',
        results: 'A horizontally scalable consumer-group architecture with exactly-once semantics and live real-time aggregation visualisation.',
        lessonsLearned: 'Exactly-once semantics are far easier to design in from the start than to retrofit. Once an aggregate can silently double-count under a specific failure condition, finding every place that assumption leaked in is much harder than building it in correctly the first time.'
      }
    },
    'End-to-End SQL Pipeline Portfolio': {
      time: '2026',
      category: 'Data Warehousing & Analytics',
      caseStudy: {
        problem: 'A single flat table can\'t answer "what did this customer\'s profile look like at the time of this transaction" once that customer\'s attributes have changed since. Historical state gets lost.',
        requirements: 'Preserve full historical change timelines for customer dimensions, not just current state; support genuinely cross-platform analytical questions; and structure data so complex queries are tractable rather than requiring ad-hoc joins across raw tables.',
        architecture: 'A multi-tier data lake pattern. CSV staging in S3, OLTP-style models for transactional accuracy, then a star schema warehouse in PostgreSQL for analytical querying.',
        dataFlow: 'Raw CSVs staged in S3 → loaded into OLTP-style models via SQLAlchemy → transformed into a star schema warehouse, with SCD Type 2 applied specifically to customer dimension changes → analytical queries run against the warehouse.',
        techDecisions: 'SCD Type 2 (versioned rows with valid-from/valid-to ranges) over simply overwriting dimension values, because the whole point of the warehouse was to answer historical questions correctly, not just reflect current state. Recursive CTEs over application-side loops for hierarchical/sequential analysis, since the database is far better positioned to do that work set-based than Python is row-by-row.',
        implementation: 'Customer dimension changes are captured with SCD Type 2 versioning, so a query against any historical date returns the customer\'s attributes as they actually were at that time, not as they are now.',
        dataQuality: 'The star schema\'s fact/dimension separation, combined with SCD Type 2 on dimensions, means historical queries are correct by construction rather than depending on the analyst remembering that "current state" doesn\'t equal "state at the time."',
        errorHandling: 'Staging data in S3 before it touches the OLTP or warehouse layers means a bad load can be re-run from the staged source without re-extracting from the original files.',
        performance: 'Recursive CTEs push sequential/hierarchical analysis down into PostgreSQL\'s query engine, which is materially faster than pulling data out and looping over it in application code.',
        observability: 'The multi-tier structure (staging → OLTP → warehouse) means a data quality issue can be isolated to a specific tier rather than requiring a full end-to-end investigation.',
        security: 'S3 staging and the warehouse layer use separate access scopes, so credentials for raw file staging don\'t also grant access to the modelled warehouse.',
        results: 'A working star schema warehouse with SCD Type 2 customer history and recursive CTE queries surfacing cross-platform revenue shifts, fraud signals, and retention metrics.',
        lessonsLearned: 'SCD Type 2 is more upfront modelling work than just overwriting rows, but it\'s the difference between a warehouse that can actually answer "why did this change" questions and one that can only ever describe the present.'
      }
    },
    'Streaming Pipeline': {
      time: '2026',
      category: 'Real-Time Data Systems',
      caseStudy: {
        problem: 'Continuous data streams need to be ingested and analysed as they arrive, not batched and processed after the fact.',
        requirements: 'Scalable ingestion that keeps up with a continuous stream, a processing layer that transforms data in near real time, and analytics that stay current with incoming data rather than lagging behind it.',
        architecture: 'A Python-based streaming pipeline covering ingestion, processing, transformation, and analytics as distinct stages for continuous data streams.',
        dataFlow: 'Continuous stream ingested → processed and transformed in near real time → surfaced for analytics.',
        techDecisions: 'Python across all four stages (ingestion, processing, transformation, analytics) to keep the pipeline maintainable as one coherent codebase rather than mixing languages across stages.',
        implementation: 'The pipeline is structured as four distinct stages so continuous data keeps moving through it without needing to be captured and processed in discrete batches.',
        dataQuality: 'Processing and transformation are kept as separate stages specifically so data can be validated and shaped before it reaches the analytics layer.',
        errorHandling: 'Stage separation means an issue in one part of the pipeline, like transformation, doesn\'t require rebuilding the ingestion or processing logic to fix.',
        performance: 'Built specifically for scalable ingestion of continuous streams, rather than for one-off batch loads.',
        observability: 'The staged architecture makes it possible to inspect data at each point in the pipeline rather than only at the final output.',
        security: 'As an exploratory project, security wasn\'t the primary focus. The emphasis was on getting a working streaming architecture end to end.',
        results: 'A working end-to-end streaming pipeline covering ingestion through analytics for continuous data streams.',
        lessonsLearned: 'Structuring the pipeline as four explicit stages, rather than one continuous script, made it much easier to reason about where in the pipeline a given piece of data actually was at any point in time.'
      }
    },
    'Early Portfolio Site': {
      time: 'Earlier project',
      category: 'Personal Site',
      caseStudy: {
        problem: 'Early on, I needed a public, deployable showcase of my work. Without one, there was no way for anyone outside a direct conversation to see what I\'d actually built.',
        requirements: 'Something realistic to ship solo, host for free, and iterate on as my skill set and project list grew.',
        architecture: 'A personal portfolio site built and published under my earlier GitHub handle, before I consolidated my work under this account.',
        dataFlow: 'Not applicable. This was a personal site project, not a data pipeline.',
        techDecisions: 'Kept the stack simple and shippable rather than reaching for infrastructure I hadn\'t yet needed to learn. The goal was getting something real online, not demonstrating every tool at once.',
        implementation: 'Built and iterated on solo, as my first real public-facing project.',
        dataQuality: 'Not applicable to a personal site project.',
        errorHandling: 'Not applicable to a personal site project.',
        performance: 'Not a focus area. The goal was existing online, not optimisation.',
        observability: 'Not applicable to a personal site project.',
        security: 'Not applicable to a personal site project.',
        results: '19 stars and 1 fork on a project with no promotion behind it. Modest but genuine external interest in an early personal site.',
        lessonsLearned: 'Building this first version directly informed decisions in my current portfolio. From picking a maintainable content structure to being deliberate about what a portfolio should actually communicate to a visitor, rather than just listing tools.'
      }
    }
  };

  const CASE_STUDY_LABELS = [
    ['problem', 'Problem'],
    ['requirements', 'Requirements'],
    ['architecture', 'Architecture'],
    ['dataFlow', 'Data Flow'],
    ['techDecisions', 'Technology Decisions'],
    ['implementation', 'Implementation'],
    ['dataQuality', 'Data Quality'],
    ['errorHandling', 'Error Handling'],
    ['performance', 'Performance'],
    ['observability', 'Observability'],
    ['security', 'Security'],
    ['results', 'Results'],
    ['lessonsLearned', 'Lessons Learned']
  ];

  const projectModal = {
    overlay: document.getElementById('projectModalOverlay'),
    title: document.getElementById('projectModalTitle'),
    image: document.getElementById('projectModalImage'),
    time: document.getElementById('projectModalTime'),
    category: document.getElementById('projectModalCategory'),
    description: document.getElementById('projectModalDescription'),
    stack: document.getElementById('projectModalStack'),
    caseStudySection: document.getElementById('projectModalCaseStudySection'),
    features: document.getElementById('projectModalFeatures'),
    featuresSection: document.getElementById('projectModalFeaturesSection'),
    github: document.getElementById('projectModalGithub'),
    closeBtn: document.getElementById('projectModalClose'),

    init() {
      this.closeBtn.addEventListener('click', () => this.close());
      this.overlay.addEventListener('click', (e) => {
        if (e.target === this.overlay) this.close();
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen()) this.close();
      });
    },

    open(data) {
      const extended = projectExtendedData[data.title] || {};
      
      this.title.textContent = data.title;
      this.image.src = data.img || 'assets/images/1.jpeg';
      this.time.textContent = extended.time || 'Project Completion: 2026';
      this.category.textContent = ' · ' + (extended.category || 'Engineering');
      this.description.textContent = data.desc;
      
      // Render Stack
      this.stack.innerHTML = (data.stack || []).map(t => `<span class="stack-badge">${t}</span>`).join('');
      
      // Render Case Study (13-point breakdown) if present
      if (extended.caseStudy) {
        this.featuresSection.style.display = 'none';
        this.caseStudySection.innerHTML = '<div class="project-modal-section-title">Engineering Case Study</div>' +
          CASE_STUDY_LABELS.map(([key, label], i) => {
            const text = extended.caseStudy[key];
            if (!text) return '';
            const num = String(i + 1).padStart(2, '0');
            return `<div class="case-study-item"><span class="case-study-num">${num}</span><div class="case-study-body"><div class="case-study-label">${label}</div><div class="case-study-text">${text}</div></div></div>`;
          }).join('');
      } else if (extended.features && extended.features.length) {
        this.caseStudySection.innerHTML = '';
        this.featuresSection.style.display = 'block';
        this.features.innerHTML = extended.features.map(f => `<li>${f}</li>`).join('');
      } else {
        this.caseStudySection.innerHTML = '';
        this.featuresSection.style.display = 'none';
      }
      
      if (data.view) {
        this.github.style.display = '';
        this.github.href = data.view;
        this.github.textContent = 'GitHub Repository';
      } else {
        this.github.style.display = 'none';
      }
      
      this.overlay.style.display = 'flex';
      this.overlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    },

    close() {
      this.overlay.style.display = 'none';
      this.overlay.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    },

    isOpen() {
      return this.overlay.style.display === 'flex';
    }
  };

  window.openProjectModal = (data) => projectModal.open(data);
  window.closeProjectModal = () => projectModal.close();

  // Skill Modal Management
  const projectLookup = {
    'PesaGuard': {title: 'PesaGuard', desc: 'Real-time M-Pesa reconciliation and anomaly detection SaaS for Kenyan SACCOs, e-commerce operators, and small fintechs, built on a Flask backend and Next.js 14 frontend.', stack: ['Flask', 'Python', 'Next.js', 'PostgreSQL', 'Daraja API'], img: 'assets/images/5.jpeg', view: ''},
    'Cloud ETL Pipeline': {title: 'Cloud ETL Pipeline', desc: 'Processed 1.6M+ records at ~70,000 rows/sec with peak memory under 300MB via chunked reading and automatic encoding detection. Idempotent batch upserts and aggregation-based deduplication give the pipeline fault tolerance, cutting full load time from 4 minutes to 45 seconds.', stack: ['Python', 'Pandas', 'PostgreSQL', 'SQLAlchemy', 'Docker', 'Pytest', 'GitHub Actions'], img: 'assets/images/2.jpeg', view: 'https://github.com/Victor-Kipruto-Rop/cloud-etl-pipeline'},
    'M-Pesa Airflow Transaction Pipeline': {title: 'M-Pesa Airflow Transaction Pipeline', desc: 'DAG-orchestrated M-Pesa transaction processing with a Faker-driven synthetic data generator, a rule-engine-based multi-stage cleaning pipeline, and a Docker Compose stack reproducible with a single command.', stack: ['Apache Airflow', 'Python', 'Faker', 'PostgreSQL', 'Docker Compose', 'Pytest', 'GitHub Actions'], img: 'assets/images/3.jpeg', view: 'https://github.com/Victor-Kipruto-Rop/mpesa_safaricom-pipeline-'},
    'Real-Time Transaction Streaming System': {title: 'Real-Time Transaction Streaming System', desc: 'A Kafka producer/consumer model for live transaction ingestion with real-time aggregation and low-latency throughput, consumer-group design for horizontal scalability, exactly-once semantics to prevent double-counting, and live Plotly visualisations inside Jupyter.', stack: ['Apache Kafka', 'Python', 'Jupyter', 'Plotly', 'Docker Compose', 'GitHub Actions'], img: 'assets/images/4.jpeg', view: 'https://github.com/Victor-Kipruto-Rop/Real_Time_Transaction_Streaming-MPESA-'},
    'End-to-End SQL Pipeline Portfolio': {title: 'End-to-End SQL Pipeline Portfolio', desc: 'A multi-tier data lake pattern from CSV staging through OLTP models into a star schema warehouse, with SCD Type 2 deployed on customer dimensions to preserve full historical change timelines, and recursive CTE queries surfacing cross-platform revenue shifts, fraud signals, and retention metrics.', stack: ['Python', 'PostgreSQL', 'AWS S3', 'SQLAlchemy', 'SCD Type 2'], img: 'assets/images/3.jpeg', view: ''},
    'Streaming Pipeline': {title: 'Streaming Pipeline', desc: 'A real-time data streaming pipeline for scalable ingestion, processing, transformation, and analytics of continuous data streams.', stack: ['Python'], img: 'assets/images/4.jpeg', view: 'https://github.com/Victor-Kipruto-Rop/streaming-pipeline'},
    'Early Portfolio Site': {title: 'Early Portfolio Site', desc: 'My first public portfolio project, built under an earlier GitHub handle before consolidating my work under this account.', stack: ['Python'], img: 'assets/images/5.jpeg', view: 'https://github.com/Victor-Kipruto-Rop/kipruto45-victor-kipruto-rop-portfolio'}
  };

  const skillData = {
    'Apache Airflow': {
      why: "Airflow gives pipelines explicit dependencies, retries, and visibility instead of a black-box cron job. When something fails at 2am, I can see exactly which task and why.",
      where: "Building the DAG-orchestrated ETL pipeline for M-Pesa transaction processing, with each cleaning stage as an independently retryable task.",
      project: "M-Pesa Airflow Transaction Pipeline"
    },
    'ETL Design': {
      why: "A pipeline is only as trustworthy as its weakest transformation step. I design each stage to be testable and reversible in isolation.",
      where: "Structuring the ingestion-to-warehouse flow so validation and deduplication run as separate, composable stages rather than one monolithic transform.",
      project: "Cloud ETL Pipeline"
    },
    'DAG Management': {
      why: "Explicit task dependencies make failure modes predictable. I'd rather see a DAG fail loudly at the right node than silently pass bad data downstream.",
      where: "Managing task-level retries, failure states, and dependency ordering across the M-Pesa pipeline's Airflow DAGs.",
      project: "M-Pesa Airflow Transaction Pipeline"
    },
    'Apache Kafka': {
      why: "Real financial events don't wait for a batch window. Kafka lets the system react to a transaction the moment it happens, not hours later.",
      where: "Building a Kafka producer/consumer model for live transaction ingestion with real-time aggregation and low-latency throughput.",
      project: "Real-Time Transaction Streaming System"
    },
    'Stream Processing': {
      why: "Fraud and anomaly windows are measured in seconds, not overnight ETL runs. Stream processing is what makes real-time monitoring possible at all.",
      where: "Aggregating streaming transaction data in real time with a consumer-group design built for horizontal scalability.",
      project: "Real-Time Transaction Streaming System"
    },
    'Producers & Consumers': {
      why: "Decoupling producers from consumers means the ingestion layer and the processing layer can fail, scale, or deploy independently.",
      where: "Designing the producer/consumer model with exactly-once semantics to prevent double-counting in downstream aggregations.",
      project: "Real-Time Transaction Streaming System"
    },
    'Star Schema': {
      why: "A well-designed star schema means analysts can write a five-line query instead of a five-join nightmare.",
      where: "Designing a star schema warehouse in a multi-tier data lake pattern, from CSV staging through OLTP models.",
      project: "End-to-End SQL Pipeline Portfolio"
    },
    'Dimensional Modelling': {
      why: "Kimball-style modelling keeps the business logic in the schema, not scattered across a dozen ad-hoc queries.",
      where: "Deploying SCD Type 2 on customer dimensions to preserve full historical change timelines.",
      project: "End-to-End SQL Pipeline Portfolio"
    },
    'OLAP Queries': {
      why: "Multi-dimensional analysis only works if the underlying queries are actually fast. I optimize for the questions the business will ask, not just the ones it's asked so far.",
      where: "Writing recursive CTE queries to surface cross-platform revenue shifts, fraud signals, and customer retention metrics.",
      project: "End-to-End SQL Pipeline Portfolio"
    },
    'Data Warehousing': {
      why: "A warehouse is only a \"single source of truth\" if people actually trust it. That trust is earned through consistent, validated loads.",
      where: "Building a multi-tier data lake pattern. From CSV staging through OLTP models into a star schema warehouse.",
      project: "End-to-End SQL Pipeline Portfolio"
    },
    'Deduplication': {
      why: "Safaricom retries webhook deliveries. Treating duplicates as a certainty rather than an edge case is what keeps a ledger honest.",
      where: "Implementing idempotency-key based deduplication so a retried webhook can never be double-counted.",
      project: "PesaGuard"
    },
    'Validation Rule Engines': {
      why: "Catching a bad record at the earliest possible stage is far cheaper than debugging a corrupted dashboard three steps downstream.",
      where: "Building a config-driven rule engine for the multi-stage cleaning pipeline. Rules are configurable, not hardcoded.",
      project: "M-Pesa Airflow Transaction Pipeline"
    },
    'Anomaly Detection': {
      why: "Reconciliation isn't just matching. It's knowing when something doesn't match, and surfacing that fast enough for someone to act on it.",
      where: "Powering the open-anomalies count on the PesaGuard admin dashboard.",
      project: "PesaGuard"
    },
    'Docker': {
      why: "\"Works on my machine\" isn't an acceptable failure mode. Containerizing a pipeline means CI runs the exact same environment as my laptop.",
      where: "Separating Extract, Transform, and Load into independent Docker microservices with exponential-backoff retry on transient failures.",
      project: "Cloud ETL Pipeline"
    },
    'GitHub Actions': {
      why: "Tests that only run when I remember to run them aren't really tests. CI makes validation non-optional.",
      where: "Gating every push with an automated Pytest suite before code reaches a trusted branch.",
      project: "Cloud ETL Pipeline"
    },
    'Pytest': {
      why: "Data engineering code fails silently more often than it crashes loudly. A real test suite is what catches that before production does.",
      where: "Testing the validation-engine and idempotency logic that the reconciliation system depends on.",
      project: "PesaGuard"
    },
    'CI/CD Pipelines': {
      why: "Frequent, low-risk deploys beat rare, high-risk ones. Automation is what makes that trade-off possible.",
      where: "Automating the build-test-deploy flow for the ETL pipeline via GitHub Actions.",
      project: "Cloud ETL Pipeline"
    },
    'Python': {
      why: "Python is where I express most of my engineering logic. From ingestion scripts to reconciliation engines to test suites.",
      where: "Writing the Flask backend, reconciliation engine, and idempotency guards across models.py and reconciliation_engine.py.",
      project: "PesaGuard"
    },
    'SQL': {
      why: "Most \"the pipeline is slow\" problems are actually \"the query is slow\" problems. SQL fluency is non-negotiable for this work.",
      where: "Writing recursive CTE queries to surface cross-platform revenue shifts, fraud signals, and customer retention metrics across a multi-tier data lake.",
      project: "End-to-End SQL Pipeline Portfolio"
    },
    'PostgreSQL': {
      why: "I default to Postgres because its reliability and tooling let me spend time on the data model, not fighting the database.",
      where: "Tuning connection pooling and batch execution size to cut a 1.6M+ row load from 4 minutes down to 45 seconds.",
      project: "Cloud ETL Pipeline"
    },
    'Git': {
      why: "A clean commit history is documentation. I use branching and commit discipline so the reasoning behind a change is never lost.",
      where: "Managing version control and collaborative workflows across every project in this portfolio.",
      project: "Cloud ETL Pipeline"
    },
    'Docker Compose': {
      why: "Local development should mirror production topology. Compose lets me spin up the full multi-service stack with one command.",
      where: "Containerising the complete Airflow and PostgreSQL stack so the environment is fully reproducible with a single command.",
      project: "M-Pesa Airflow Transaction Pipeline"
    },
    'MySQL': {
      why: "Being fluent across both PostgreSQL and MySQL means I'm not locked into one vendor's quirks when a team already has infrastructure decisions made.",
      where: "Applying relational database fundamentals, schema design, window functions, and complex CTEs, interchangeably across PostgreSQL and MySQL.",
      project: "Cloud ETL Pipeline"
    },
    'Shell / Bash': {
      why: "Automation lives in the shell. CI steps, container entrypoints, and quick data checks all start with a script, not a GUI.",
      where: "Scripting CI/CD automation steps and container orchestration commands across every pipeline project.",
      project: "Cloud ETL Pipeline"
    },
    'AWS (S3, EC2)': {
      why: "Cloud-native storage and compute are the default for production data infra. S3 for durable object storage, EC2 when I need control over the runtime.",
      where: "Using S3 as the ingestion source for a cloud-hosted pipeline processing 1.6M+ rows at 70,000 rows/sec.",
      project: "Cloud ETL Pipeline"
    },
    'Pandas': {
      why: "Pandas is where exploratory data wrangling happens fast. Before a transformation earns a permanent place in a pipeline, I prototype it in a DataFrame.",
      where: "Writing the custom deduplication logic that aggregates quantities on conflicting records instead of dropping them.",
      project: "Cloud ETL Pipeline"
    },
    'NumPy': {
      why: "Vectorized operations matter once a dataset gets large enough that a Python for-loop becomes the actual bottleneck.",
      where: "Supporting numerical operations underneath the Pandas-based transformation logic in the market data ETL pipeline.",
      project: "Cloud ETL Pipeline"
    },
    'SQLAlchemy': {
      why: "An ORM layer means the same codebase can target different databases without rewriting every query by hand.",
      where: "Managing the PostgreSQL output layer and connection handling across the ETL pipeline's database interactions.",
      project: "Cloud ETL Pipeline"
    },
    'Faker': {
      why: "Testing a pipeline against realistic data, not just placeholder strings, catches edge cases that synthetic filler data never will.",
      where: "Generating a configurable synthetic data feed with realistic Kenyan phone number distributions for pipeline testing.",
      project: "M-Pesa Airflow Transaction Pipeline"
    },
    'Grafana': {
      why: "A pipeline without a dashboard is a pipeline nobody's actually watching. Grafana turns pipeline output into something a team can monitor live.",
      where: "Connecting the PostgreSQL output layer to live operational dashboards tracking market data trends.",
      project: "Cloud ETL Pipeline"
    },
    'Plotly': {
      why: "Interactive charts let you actually explore an anomaly instead of squinting at a static image.",
      where: "Producing live visualisation outputs directly from the Kafka consumer layer for immediate feedback on streaming data.",
      project: "Real-Time Transaction Streaming System"
    },
    'Jupyter Notebooks': {
      why: "Notebooks are where I validate an idea against real data before it becomes production code. Fast iteration matters before commitment.",
      where: "Prototyping streaming data visualisations and validating consumer output during development of the transaction streaming system.",
      project: "Real-Time Transaction Streaming System"
    },
    'SCD Type 2': {
      why: "Overwriting a dimension record destroys history. SCD Type 2 preserves every version of the truth, which matters when you need to know what was believed last quarter.",
      where: "Deploying Type 2 slowly-changing dimensions on customer records to preserve full historical change timelines.",
      project: "End-to-End SQL Pipeline Portfolio"
    }
  };

  const skillModal = {
    overlay: document.getElementById('skillModalOverlay'),
    body: document.getElementById('skillModalBody'),
    title: document.getElementById('skillModalTitle'),
    closeBtn: document.getElementById('skillModalClose'),

    init() {
      this.closeBtn.addEventListener('click', () => this.close());
      this.overlay.addEventListener('click', (e) => {
        if (e.target === this.overlay) this.close();
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen()) this.close();
      });
    },

    open(skillName) {
      const data = skillData[skillName];
      this.title.textContent = skillName;
      if (!data) {
        this.body.innerHTML = '<p style="margin:0;">Details coming soon...</p>';
      } else {
        const proj = projectLookup[data.project];
        this.body.innerHTML = `
          <div class="skill-detail-block">
            <p class="skill-detail-label">Why I Use It</p>
            <p class="skill-detail-text">${data.why}</p>
          </div>
          <div class="skill-detail-block">
            <p class="skill-detail-label">Where I've Used It</p>
            <p class="skill-detail-text">${data.where}</p>
          </div>
          <div class="skill-detail-block" style="margin-bottom:0;">
            <p class="skill-detail-label">Project</p>
            <button type="button" class="skill-detail-project-link" id="skillDetailProjectBtn">${data.project} <i class="fas fa-arrow-up-right-from-square"></i></button>
          </div>
        `;
        const projBtn = document.getElementById('skillDetailProjectBtn');
        if (projBtn && proj) {
          projBtn.addEventListener('click', () => {
            this.close();
            openProjectModal(proj);
          });
        }
      }
      this.overlay.style.display = 'flex';
      this.overlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    },

    close() {
      this.overlay.style.display = 'none';
      this.overlay.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    },

    isOpen() {
      return this.overlay.style.display === 'flex';
    }
  };

  window.openSkillModal = (name) => skillModal.open(name);
  window.closeSkillModal = () => skillModal.close();

  // Modal management
  const subscriptionModal = {
    overlay: document.getElementById('subscriptionModalOverlay'),
    modal: document.querySelector('.subscription-modal'),
    closeBtn: document.getElementById('subscriptionModalClose'),
    rssUrlInput: document.getElementById('rssUrlInput'),
    copyRssBtn: document.getElementById('copyRssBtn'),
    notification: document.getElementById('subscriptionNotification'),

    init() {
      subscriptionAnalytics.init();
      this.setupEventListeners();
    },

    setupEventListeners() {
      this.closeBtn.addEventListener('click', () => this.close());
      this.overlay.addEventListener('click', (e) => {
        if (e.target === this.overlay) this.close();
      });

      document.querySelectorAll('.subscription-tab').forEach(tab => {
        tab.addEventListener('click', (e) => this.switchTab(e.target.closest('button').dataset.tab));
      });

      document.querySelectorAll('[data-option]').forEach(option => {
        option.addEventListener('click', (e) => this.handleFeedOption(e.target.closest('[data-option]').dataset.option));
      });

      document.getElementById('emailTab').addEventListener('submit', (e) => this.handleEmailSubmit(e));

      this.copyRssBtn.addEventListener('click', () => this.copyRssUrl());

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen()) this.close();
      });
    },

    open() {
      this.overlay.style.display = 'flex';
      this.overlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    },

    close() {
      this.overlay.style.display = 'none';
      this.overlay.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    },

    isOpen() {
      return this.overlay.style.display === 'flex';
    },

    switchTab(tabName) {
      document.querySelectorAll('.subscription-tab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
      });

      document.querySelectorAll('.subscription-form').forEach(form => {
        form.style.display = form.id === tabName + 'Tab' ? 'block' : 'none';
      });

      document.getElementById('rssUrlSection').style.display = tabName === 'feed' ? 'block' : 'none';
    },

    handleFeedOption(option) {
      subscriptionAnalytics.track(option + '_clicks');

      const rssUrl = 'https://www.victorkipruto.com/rss.xml';
      const inoreaderUrl = 'https://www.inoreader.com/?add_feed=' + encodeURIComponent(rssUrl);
      const feedlyUrl = 'https://feedly.com/i/subscription/feed/' + encodeURIComponent(rssUrl);

      const urls = {
        rss: rssUrl,
        inoreader: inoreaderUrl,
        feedly: feedlyUrl,
        'copy-url': null
      };

      if (option === 'copy-url') {
        this.copyRssUrl();
      } else if (urls[option]) {
        window.open(urls[option], '_blank');
        this.showNotification();
      }
    },

    handleEmailSubmit(e) {
      e.preventDefault();

      const name = document.getElementById('emailName').value.trim();
      const email = document.getElementById('emailAddress').value.trim();

      if (!name || !email) return;

      const subscribers = JSON.parse(localStorage.getItem('emailSubscribers') || '[]');
      const subscriber = { name, email, date: new Date().toISOString() };

      if (!subscribers.some(s => s.email === email)) {
        subscribers.push(subscriber);
        localStorage.setItem('emailSubscribers', JSON.stringify(subscribers));
        subscriptionAnalytics.track('email_subscriptions');
      }

      document.getElementById('emailTab').reset();
      this.showNotification();
      setTimeout(() => this.close(), 2000);
    },

    copyRssUrl() {
      const url = this.rssUrlInput.value;
      navigator.clipboard.writeText(url).then(() => {
        subscriptionAnalytics.track('copy_clicks');
        const originalText = this.copyRssBtn.innerHTML;
        this.copyRssBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
          this.copyRssBtn.innerHTML = originalText;
        }, 2000);
      });
    },

    showNotification() {
      this.notification.style.display = 'block';
      setTimeout(() => {
        this.notification.style.display = 'none';
      }, 4000);
    }
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      subscriptionModal.init();
      skillModal.init();
      projectModal.init();
    });
  } else {
    subscriptionModal.init();
    skillModal.init();
    projectModal.init();
  }

  // Expose for external access
  window.openSubscriptionModal = () => subscriptionModal.open();
  window.getSubscriptionAnalytics = () => subscriptionAnalytics.getAll();

  // Scroll progress bar
  const scrollProgress = document.getElementById('scrollProgress');
  function updateScrollProgress() {
    if (!scrollProgress) return;
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    scrollProgress.style.width = pct + '%';
  }
  window.addEventListener('scroll', updateScrollProgress, { passive: true });
  window.addEventListener('resize', updateScrollProgress);
  updateScrollProgress();

(function () {
    const topFab = document.getElementById('scrollToTopFab');
    if (!topFab) return;
    const SHOW_AFTER = 400;
    function toggleTopFab() {
      if (window.scrollY > SHOW_AFTER) {
        topFab.classList.add('is-visible');
      } else {
        topFab.classList.remove('is-visible');
      }
    }
    topFab.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    window.addEventListener('scroll', toggleTopFab, { passive: true });
    toggleTopFab();
  })();

  // Floating WhatsApp button: footer-docking (so it never overlaps the
  // footer) + the greeting tooltip's scroll-triggered reveal, both driven
  // by one requestAnimationFrame-throttled scroll handler for performance.
  (function () {
    const footer = document.querySelector('footer');
    const dockedFabs = Array.from(document.querySelectorAll('.fab'));
    const tooltip = document.getElementById('chatTooltip');
    const closeBtn = document.getElementById('chatTooltipClose');
    if (!footer && !tooltip) return;

    const DOCK_GAP = 24;       // px above the footer's top edge for the FABs
    const TOOLTIP_STACK = 70;  // extra px so the tooltip docks above the FAB, not on top of it
    const REVEAL_AFTER = 200;  // px scrolled before the tooltip appears
    const DISMISS_KEY = 'chatTooltipDismissed';

    let dismissed = false;
    try { dismissed = sessionStorage.getItem(DISMISS_KEY) === '1'; } catch (err) { /* storage unavailable */ }
    let revealed = false; // once true, the tooltip stays visible until dismissed
    let ticking = false;

    function updatePositions() {
      ticking = false;

      // Dock the FABs (and the tooltip, stacked above them) once the
      // footer scrolls into view, instead of sitting fixed on top of it.
      if (footer && dockedFabs.length) {
        const footerTop = footer.getBoundingClientRect().top;
        const shouldDock = footerTop <= window.innerHeight;
        if (shouldDock) {
          const bottomOffset = Math.round(document.documentElement.scrollHeight - footer.offsetTop + DOCK_GAP);
          dockedFabs.forEach(function (fab) {
            fab.style.position = 'absolute';
            fab.style.bottom = bottomOffset + 'px';
          });
          if (tooltip) {
            tooltip.style.position = 'absolute';
            tooltip.style.bottom = (bottomOffset + TOOLTIP_STACK) + 'px';
          }
        } else {
          dockedFabs.forEach(function (fab) {
            fab.style.position = '';
            fab.style.bottom = '';
          });
          if (tooltip) {
            tooltip.style.position = '';
            tooltip.style.bottom = '';
          }
        }
      }

      // Reveal the tooltip once past the threshold; once shown it stays
      // up (per spec) regardless of further scrolling, until dismissed.
      if (tooltip && !dismissed && !revealed && window.scrollY > REVEAL_AFTER) {
        revealed = true;
        tooltip.classList.add('is-visible');
      }
    }

    function onScrollOrResize() {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(updatePositions);
      }
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dismissed = true;
        tooltip.classList.remove('is-visible');
        try { sessionStorage.setItem(DISMISS_KEY, '1'); } catch (err) { /* storage unavailable */ }
      });
    }

    window.addEventListener('scroll', onScrollOrResize, { passive: true });
    window.addEventListener('resize', onScrollOrResize);
    updatePositions();
  })();
