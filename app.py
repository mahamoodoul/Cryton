from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from dotenv import load_dotenv
from datetime import datetime
import os
import resend

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')

def send_email(to, reply_to, subject, html_body):
    resend.api_key = os.getenv('RESEND_API_KEY') or os.getenv('MAIL_PASSWORD', '')
    return resend.Emails.send({
        'from':     os.getenv('MAIL_FROM', 'onboarding@resend.dev'),
        'to':       [to],
        'reply_to': [reply_to],
        'subject':  subject,
        'html':     html_body,
    })

# ── i18n strings ──────────────────────────────────────────────────────────────
TRANSLATIONS = {
    'en': {
        'nav': {
            'services': 'Services',
            'about':    'About',
            'portfolio':'Portfolio',
            'contact':  'Contact',
            'book':     'Book a Call',
        },
        'hero': {
            'badge':    'Available for new projects — Oslo, Norway',
            'h1a':      'Building',
            'h1b':      'Secure',
            'h1c':      '& Scalable Digital Solutions',
            'sub':      'We help businesses modernize with cloud infrastructure, smart automation, and enterprise-grade security.',
            'cta1':     'Book Consultation',
            'cta2':     'Explore Services',
        },
        'stats': [
            {'num': '5+',  'label': 'Service areas'},
            {'num': '20+', 'label': 'Projects delivered'},
            {'num': 'Oslo','label': 'Based in Norway'},
        ],
        'services': {
            'label': 'What we do',
            'title': 'End-to-end tech consulting',
            'sub':   'Practical consulting across cloud, data, security, and automation — delivered end to end.',
            'list': [
                {'icon':'ti-cloud',      'img':'cloud.svg',      'name':'Cloud Solutions',   'desc':'AWS-native architecture, DevOps pipelines, and infrastructure built to scale.'},
                {'icon':'ti-database',   'img':'data.svg',       'name':'Data Engineering',  'desc':'ETL pipelines, Databricks warehouses, and dashboards that turn data into decisions.'},
                {'icon':'ti-shield-lock','img':'security.svg',   'name':'Cybersecurity',     'desc':'Zero-trust auth, API hardening, and cloud security assessments.'},
                {'icon':'ti-bolt',       'img':'automation.svg', 'name':'Automation',        'desc':'Power Platform workflows, self-service portals, and no-code automation.'},
                {'icon':'ti-code',       'img':'software.svg',   'name':'Custom Software',   'desc':'Web apps, REST APIs, and internal tools built to your exact specification.'},
            ],
        },
        'process': {
            'label': 'How we work',
            'title': 'A clear, structured process',
            'steps': [
                {'num':'01 / DISCOVER','title':'Understand your needs',  'desc':'We audit your stack, surface pain points, and align on goals — before writing a single line.'},
                {'num':'02 / DESIGN',  'title':'Architect the solution', 'desc':'A roadmap tailored for security, scale, and your team\'s capacity to execute.'},
                {'num':'03 / BUILD',   'title':'Deliver with precision', 'desc':'Iterative delivery with clear milestones, documentation, and continuous feedback.'},
                {'num':'04 / SUPPORT', 'title':'Optimize & maintain',    'desc':'Post-launch monitoring, performance tuning, and improvements as your business grows.'},
            ],
        },
        'portfolio': {
            'label': 'Our work',
            'title': ' Projects',
            'sub':   'A sample of what we have delivered for our clients.',
            'list': [
                {'tag':'Cloud Engineering', 'img':'aws.svg',       'slug':'aws-migration',      'name':'Multi-region AWS migration',    'desc':'Zero-downtime migration to a multi-region AWS setup, cutting infrastructure costs by 30%.'},
                {'tag':'Data Engineering',  'img':'analytics.svg', 'slug':'analytics-pipeline', 'name':'Real-time analytics pipeline', 'desc':'Databricks pipeline processing 5M+ daily events with sub-second latency and automated alerting.'},
                {'tag':'Cybersecurity',     'img':'auth.svg',      'slug':'zero-trust-auth',    'name':'Zero-trust auth system',       'desc':'OAuth 2.0 + OIDC with role-based access control deployed across three enterprise platforms.'},
                {'tag':'Automation',        'img':'hr-portal.svg', 'slug':'hr-portal',          'name':'Power Platform HR portal',     'desc':'Self-service HR portal with automated approval workflows on Power Apps and Power Automate.'},
            ],
        },
        'cta': {
            'h2':  'Ready to modernize your infrastructure?',
            'sub': 'Let\'s discuss your next project — no commitment, just clarity.',
            'btn': 'Book a free call →',
        },
        'contact': {
            'label':       'Get in touch',
            'title':       'Let\'s build something great',
            'sub':         'Tell us about your project and we\'ll get back to you within one business day.',
            'name':        'Full name',
            'email':       'Email address',
            'company':     'Company (optional)',
            'service':     'Service of interest',
            'message':     'Tell us about your project',
            'submit':      'Send message',
            'success':     'Message sent! We\'ll be in touch within 24 hours.',
            'error':       'Something went wrong. Please try again or email us directly.',
            'service_opts':['Cloud Solutions','Data Engineering','Cybersecurity','Automation','Custom Software','Other'],
        },
        'footer': {
            'tagline': 'Secure. Scalable. Intelligent.',
            'copy':    f'© {datetime.now().year} Cryton · Oslo, Norway',
        },
        'about': {
            'label': 'About us',
            'title': 'Technology built on trust',
            'body':  'Cryton was founded to help businesses adopt secure, modern technology. We combine cloud engineering, software development, data systems, and cybersecurity to build efficient digital solutions tailored to your needs.',
            'mission_title': 'Mission',
            'mission': 'Reliable, scalable technology that empowers businesses through innovation and security.',
            'vision_title': 'Vision',
            'vision': 'A trusted technology partner for every business ready to transform digitally.',
        },
        'case_study': {
            'back':        '← Back to projects',
            'challenge':   'The Challenge',
            'solution':    'Our Approach',
            'outcome':     'The Outcome',
            'tech_label':  'Tech stack',
            'timeline_label': 'Project timeline',
            'cta_label':   'Start a similar project',
            'cta_sub':     'Tell us about your goals and we\'ll get back within one business day.',
            'cta_btn':     'Book a free consultation →',
        },
        'case_studies': {
            'aws-migration': {
                'tag':      'Cloud Engineering',
                'img':      'aws.svg',
                'name':     'Multi-region AWS migration',
                'subtitle': 'Zero-downtime cutover to a multi-region setup — 30% cost reduction, 99.99% uptime.',
                'overview': 'A Norwegian SaaS company needed to migrate their monolithic deployment to a resilient multi-region AWS architecture without impacting 40,000+ daily active users. Cryton designed and executed the migration with a 4-minute read-only window — no alerts, no SLA breaches.',
                'challenge': 'The client ran a single-region EU deployment with no failover, creating unacceptable risk for a platform with contractual uptime SLAs. Any outage window would erode client trust and trigger financial penalties. Infrastructure was provisioned by hand, with no IaC and no rollback capability.',
                'solution': 'We designed a multi-region active-passive architecture across us-east-1 and eu-west-1, with Route 53 latency-based routing and automated DNS failover. All infrastructure was codified in Terraform — replacing 100% of manual provisioning. RDS Aurora Global Database provided sub-second replica lag. A phased cutover runbook with automated rollback gates ensured zero risk on go-live day.',
                'outcome': 'The live cutover completed in a single 4-minute maintenance window. Infrastructure costs fell 30% through Reserved Instances and right-sized compute. The client now has a fully automated DR procedure with a tested RTO under 60 seconds.',
                'metrics': [
                    {'num': '30%',    'label': 'Cost reduction'},
                    {'num': '4 min',  'label': 'Cutover window'},
                    {'num': '99.99%', 'label': 'Uptime SLA'},
                    {'num': '<60s',   'label': 'Tested RTO'},
                ],
                'tech': ['AWS', 'Terraform', 'RDS Aurora', 'CloudFront', 'Route 53', 'ECS Fargate', 'CDK'],
                'timeline': [
                    {'phase': '01', 'title': 'Architecture audit',    'desc': 'Mapped all services, dependencies, and data flows. Identified 3 single points of failure and 14 manually provisioned resources.'},
                    {'phase': '02', 'title': 'IaC & blueprint',       'desc': 'Codified all existing infrastructure in Terraform. Designed target-state architecture and a phased cutover runbook with automated rollback gates.'},
                    {'phase': '03', 'title': 'Parallel build',        'desc': 'Provisioned the replica region in parallel with live production — zero disruption during build. Ran 2× load tests to validate replica capacity.'},
                    {'phase': '04', 'title': 'Zero-downtime cutover', 'desc': 'Traffic shifted via weighted routing over 15 minutes. DB failover tested and confirmed sub-60s RTO. Full monitoring active throughout.'},
                ],
            },
            'analytics-pipeline': {
                'tag':      'Data Engineering',
                'img':      'analytics.svg',
                'name':     'Real-time analytics pipeline',
                'subtitle': '5M+ daily events at sub-millisecond latency — live dashboards and automated business alerts.',
                'overview': 'A Nordic e-commerce platform replaced batch nightly reporting with a real-time streaming pipeline on Databricks. Product and operations teams now see live event data within seconds, enabling immediate response to sales funnel drops, inventory thresholds, and anomalous traffic.',
                'challenge': 'Existing nightly ETL jobs left the business blind to intra-day trends. Teams had no visibility into live conversion rates, cart abandonment spikes, or inventory shortfalls until the following morning — by which point revenue was already lost. The data team spent 40% of their time maintaining fragile batch scripts.',
                'solution': 'We built a streaming pipeline on Databricks with Delta Live Tables, ingesting Kafka events from 14 application services in real time. Transformations run as structured streaming jobs with schema evolution and late-arrival handling built in. Power BI connects via DirectQuery for live dashboard refreshes. Databricks SQL alerts fire Slack and email notifications within 30 seconds of threshold breaches across 12 tracked KPIs.',
                'outcome': 'The pipeline processes 5M+ events per day with end-to-end latency under 1ms for aggregated metrics. The data team\'s maintenance burden dropped 70%. The business detected and resolved a payment gateway issue within 8 minutes — previously it would have gone unnoticed overnight.',
                'metrics': [
                    {'num': '5M+',  'label': 'Events / day'},
                    {'num': '<1ms', 'label': 'Avg latency'},
                    {'num': '99.9%','label': 'Pipeline SLA'},
                    {'num': '<30s', 'label': 'Alert response'},
                ],
                'tech': ['Databricks', 'Delta Live Tables', 'Apache Kafka', 'Python', 'Power BI', 'Azure', 'SQL', 'Spark'],
                'timeline': [
                    {'phase': '01', 'title': 'Data discovery',       'desc': 'Audited all event sources, schema quality, and volume patterns across 14 application services. Identified 3 schema inconsistency classes.'},
                    {'phase': '02', 'title': 'Pipeline architecture', 'desc': 'Designed streaming topology with idempotent writes, late-arrival handling, and schema registry. Defined SLA targets and alert thresholds.'},
                    {'phase': '03', 'title': 'Build & load-test',    'desc': 'Deployed Delta Live Tables with unit-tested transformation logic. Load-tested at 2× peak volume with zero data loss.'},
                    {'phase': '04', 'title': 'Dashboards & alerts',  'desc': 'Built 6 live Power BI dashboards and configured threshold-based Slack/email alerts for 12 business KPIs.'},
                ],
            },
            'zero-trust-auth': {
                'tag':      'Cybersecurity',
                'img':      'auth.svg',
                'name':     'Zero-trust auth system',
                'subtitle': 'Unified identity across three enterprise platforms — OAuth 2.0, OIDC, and fine-grained RBAC.',
                'overview': 'A financial services firm consolidated identity management across three internal platforms into a single zero-trust auth layer. Independent user databases, inconsistent session handling, and no central revocation were flagged as critical control failures by external compliance auditors.',
                'challenge': 'Three applications maintained separate user stores and session tokens with no shared revocation capability. Revoking a compromised account required manual action in three systems — taking up to 30 minutes. Audit logs were fragmented across platforms, making compliance reporting a multi-day effort.',
                'solution': 'We deployed Keycloak as the central IdP with OAuth 2.0 Authorization Code + PKCE flows and OIDC discovery endpoints. Each platform was integrated via confidential clients with short-lived JWTs (15-min TTL) and refresh token rotation. RBAC roles were mapped from Active Directory group membership, enabling fine-grained permissions without application-level user management. A single audit stream now captures all authentication events across all three platforms.',
                'outcome': 'Revoking user access across all systems now takes under 5 seconds via a single admin action. The firm passed an external penetration test with zero critical findings and satisfied all compliance audit requirements. Compliance reporting that previously took days is now automated.',
                'metrics': [
                    {'num': '3',    'label': 'Platforms unified'},
                    {'num': '<5s',  'label': 'Access revocation'},
                    {'num': '100%', 'label': 'Audit coverage'},
                    {'num': '0',    'label': 'Pen-test findings'},
                ],
                'tech': ['Keycloak', 'OAuth 2.0', 'OIDC', 'JWT', 'RBAC', 'Active Directory', 'Python', 'Nginx'],
                'timeline': [
                    {'phase': '01', 'title': 'Security assessment',  'desc': 'Mapped auth flows across all three platforms. Documented privilege escalation paths, audit gaps, and token lifecycle vulnerabilities.'},
                    {'phase': '02', 'title': 'IdP design',           'desc': 'Configured Keycloak realm, client scopes, role mappings, and AD federation with automated group sync.'},
                    {'phase': '03', 'title': 'Platform integration', 'desc': 'Integrated each application via OIDC middleware — minimal code changes required, backward-compatible token validation throughout.'},
                    {'phase': '04', 'title': 'Pen test & go-live',  'desc': 'External penetration test passed with zero critical findings. Phased rollout over two weeks with zero user-facing disruption.'},
                ],
            },
            'hr-portal': {
                'tag':      'Automation',
                'img':      'hr-portal.svg',
                'name':     'Power Platform HR portal',
                'subtitle': 'Leave management automation — approval time cut from 3 days to 4 hours, 60% admin reduction.',
                'overview': 'A 500-person Norwegian company replaced email-based HR request handling with a self-service portal on Power Apps. Managers and employees now submit, track, and approve requests in a single interface backed by automated multi-step approval flows in Power Automate.',
                'challenge': 'Manual leave request handling averaged 3–4 email chains and 3 business days per request. HR had no real-time visibility into team leave coverage, making workforce planning reactive. Monthly payroll export was a fully manual 4-hour process. Two HR staff were spending 30% of their time on request administration.',
                'solution': 'We built a self-service HR portal on Power Apps connected to SharePoint lists for persistent storage and Dataverse for the data model. Power Automate drives multi-step approval flows: line manager → HR → payroll notification, with automatic escalation after 48 hours of inaction. The portal surfaces live team calendars, individual leave balances, and a one-click payroll export to the existing payroll system. A Power BI dashboard gives HR real-time coverage visibility across departments.',
                'outcome': 'Average approval time fell from 3 days to under 4 hours. HR administrative overhead dropped 60%, freeing the team for strategic HR work. The monthly payroll export is fully automated — 4 hours of manual work eliminated. Zero payroll errors since go-live.',
                'metrics': [
                    {'num': '3d→4h', 'label': 'Approval time'},
                    {'num': '60%',   'label': 'Admin time saved'},
                    {'num': '100%',  'label': 'Process automated'},
                    {'num': '0',     'label': 'Payroll errors'},
                ],
                'tech': ['Power Apps', 'Power Automate', 'SharePoint', 'Dataverse', 'Microsoft 365', 'Power BI'],
                'timeline': [
                    {'phase': '01', 'title': 'Process mapping',   'desc': 'Ran workshops with HR, managers, and payroll to document the full request lifecycle, decision rules, and data requirements.'},
                    {'phase': '02', 'title': 'App design',        'desc': 'Designed wireframes, data model in Dataverse, and approval logic. Signed off by HR before any build began.'},
                    {'phase': '03', 'title': 'Build & automate',  'desc': 'Built Power App with 4 screens, Power Automate flows with escalation and payroll connector, and Power BI coverage dashboard.'},
                    {'phase': '04', 'title': 'Rollout & training','desc': 'Phased rollout to 3 pilot teams with rapid feedback cycles, then company-wide deployment with self-service training guides.'},
                ],
            },
        },
    },
    'no': {
        'nav': {
            'services': 'Tjenester',
            'about':    'Om oss',
            'portfolio':'Portefølje',
            'contact':  'Kontakt',
            'book':     'Book samtale',
        },
        'hero': {
            'badge':    'Tilgjengelig for nye prosjekter — Oslo, Norge',
            'h1a':      'Vi bygger',
            'h1b':      'sikre',
            'h1c':      'og skalerbare digitale løsninger',
            'sub':      'Vi hjelper norske bedrifter med å modernisere gjennom skyinfrastruktur, smart automatisering og sikkerhet i enterprise-klassen.',
            'cta1':     'Book konsultasjon',
            'cta2':     'Utforsk tjenester',
        },
        'stats': [
            {'num': '5+',  'label': 'Tjenesteområder'},
            {'num': '20+', 'label': 'Levererte prosjekter'},
            {'num': 'Oslo','label': 'Basert i Norge'},
        ],
        'services': {
            'label': 'Hva vi gjør',
            'title': 'Helhetlig teknologirådgivning',
            'sub':   'Praktisk rådgivning innen sky, data, sikkerhet og automatisering — levert fra ende til ende.',
            'list': [
                {'icon':'ti-cloud',      'img':'cloud.svg',      'name':'Skyløsninger',             'desc':'AWS-native arkitektur, DevOps-pipelines og infrastruktur bygget for å skalere.'},
                {'icon':'ti-database',   'img':'data.svg',       'name':'Dataingeniørarbeid',       'desc':'ETL-pipelines, Databricks-lagre og dashboards som gjør data til beslutninger.'},
                {'icon':'ti-shield-lock','img':'security.svg',   'name':'Cybersikkerhet',           'desc':'Zero-trust-autentisering, API-herding og sikkerhetsvurderinger for sky.'},
                {'icon':'ti-bolt',       'img':'automation.svg', 'name':'Automatisering',           'desc':'Power Platform-arbeidsflyter, selvbetjeningsportaler og automatisering uten kode.'},
                {'icon':'ti-code',       'img':'software.svg',   'name':'Skreddersydd programvare', 'desc':'Webapper, REST-APIer og interne verktøy bygget til dine spesifikasjoner.'},
            ],
        },
        'process': {
            'label': 'Slik jobber vi',
            'title': 'En tydelig og strukturert prosess',
            'steps': [
                {'num':'01 / KARTLEGG','title':'Forstå dine behov',         'desc':'Vi kartlegger stacken din, avdekker problemer og setter klare mål — før vi skriver en eneste linje.'},
                {'num':'02 / DESIGN',  'title':'Utvikle arkitekturen',      'desc':'Et veikart tilpasset sikkerhet, skalerbarhet og teamets kapasitet til å gjennomføre.'},
                {'num':'03 / BYGG',    'title':'Lever med presisjon',       'desc':'Iterativ levering med tydelige milepæler, dokumentasjon og kontinuerlige tilbakemeldinger.'},
                {'num':'04 / SUPPORT', 'title':'Optimaliser og vedlikehold','desc':'Overvåking etter lansering, ytelsesoptimalisering og forbedringer etter hvert som du vokser.'},
            ],
        },
        'portfolio': {
            'label': 'Våre prosjekter',
            'title': 'Utvalgte prosjekter',
            'sub':   'Et utvalg av hva vi har levert for våre kunder.',
            'list': [
                {'tag':'Skyingeniørarbeid',  'img':'aws.svg',       'slug':'aws-migration',      'name':'Multi-region AWS-migrering',  'desc':'Migrering til multi-region AWS uten nedetid, med 30% reduksjon i infrastrukturkostnader.'},
                {'tag':'Dataingeniørarbeid', 'img':'analytics.svg', 'slug':'analytics-pipeline', 'name':'Sanntids analysepipeline',    'desc':'Databricks-pipeline som behandler 5M+ daglige hendelser med forsinkelse under ett sekund.'},
                {'tag':'Cybersikkerhet',     'img':'auth.svg',      'slug':'zero-trust-auth',    'name':'Zero-trust autentisering',    'desc':'OAuth 2.0 + OIDC med rollebasert tilgangskontroll på tvers av tre enterprise-plattformer.'},
                {'tag':'Automatisering',     'img':'hr-portal.svg', 'slug':'hr-portal',          'name':'Power Platform HR-portal',   'desc':'Selvbetjenings-HR-portal med automatiserte godkjenningsarbeidsflyter på Power Apps.'},
            ],
        },
        'cta': {
            'h2':  'Klar for å modernisere din infrastruktur?',
            'sub': 'La oss diskutere ditt neste prosjekt — ingen forpliktelse, bare klarhet.',
            'btn': 'Book en gratis samtale →',
        },
        'contact': {
            'label':       'Ta kontakt',
            'title':       'La oss bygge noe flott',
            'sub':         'Fortell oss om prosjektet ditt, så svarer vi innen én virkedag.',
            'name':        'Fullt navn',
            'email':       'E-postadresse',
            'company':     'Selskap (valgfritt)',
            'service':     'Ønsket tjeneste',
            'message':     'Fortell oss om prosjektet ditt',
            'submit':      'Send melding',
            'success':     'Melding sendt! Vi tar kontakt innen 24 timer.',
            'error':       'Noe gikk galt. Prøv igjen eller send oss en e-post direkte.',
            'service_opts':['Skyløsninger','Dataingeniørarbeid','Cybersikkerhet','Automatisering','Skreddersydd programvare','Annet'],
        },
        'footer': {
            'tagline': 'Sikker. Skalerbar. Intelligent.',
            'copy':    f'© {datetime.now().year} Cryton · Oslo, Norge',
        },
        'about': {
            'label': 'Om oss',
            'title': 'Teknologi bygget på tillit',
            'body':  'Cryton ble grunnlagt for å hjelpe bedrifter med å ta i bruk sikker, moderne teknologi. Vi kombinerer skyingeniørarbeid, programvareutvikling, datasystemer og cybersikkerhet for å bygge effektive digitale løsninger.',
            'mission_title': 'Misjon',
            'mission': 'Pålitelig, skalerbar teknologi som styrker bedrifter gjennom innovasjon og sikkerhet.',
            'vision_title': 'Visjon',
            'vision': 'En betrodd teknologipartner for alle bedrifter klare for digital transformasjon.',
        },
        'case_study': {
            'back':           '← Tilbake til prosjekter',
            'challenge':      'Utfordringen',
            'solution':       'Vår tilnærming',
            'outcome':        'Resultatet',
            'tech_label':     'Teknologistack',
            'timeline_label': 'Prosjektforløp',
            'cta_label':      'Start et lignende prosjekt',
            'cta_sub':        'Fortell oss om dine mål, og vi svarer innen én virkedag.',
            'cta_btn':        'Book en gratis konsultasjon →',
        },
        'case_studies': {
            'aws-migration': {
                'tag':      'Skyingeniørarbeid',
                'img':      'aws.svg',
                'name':     'Multi-region AWS-migrering',
                'subtitle': 'Migrering uten nedetid til multi-region oppsett — 30% kostnadsreduksjon, 99,99% oppetid.',
                'overview': 'En norsk SaaS-bedrift trengte å migrere fra en monolittisk distribusjon til en robust multi-region AWS-arkitektur, uten å påvirke 40 000+ daglige brukere. Cryton designet og gjennomførte migreringen med et 4-minutters vedlikeholdsvindu — ingen varsler, ingen brudd på SLA-er.',
                'challenge': 'Kunden kjørte en enkelt-region EU-distribusjon uten failover, noe som skapte uakseptabel risiko for en plattform med kontraktsfestede oppetids-SLA-er. Infrastrukturen ble provisjonert manuelt uten IaC og uten mulighet for automatisk tilbakerulling.',
                'solution': 'Vi designet en multi-region aktiv-passiv arkitektur over us-east-1 og eu-west-1, med Route 53 latensbasert ruting og automatisert DNS-failover. All infrastruktur ble kodifisert i Terraform. RDS Aurora Global Database ga replikeringsforsinkelse under ett sekund. En trinnvis cutover-plan med automatiserte tilbakerullingssteg sikret nullrisiko på leveringsdagen.',
                'outcome': 'Live cutover ble gjennomført i et 4-minutters vedlikeholdsvindu. Infrastrukturkostnadene falt med 30% gjennom Reserved Instances og riktig dimensjonert beregning. Kunden har nå et fullt automatisert DR-opplegg med testet RTO under 60 sekunder.',
                'metrics': [
                    {'num': '30%',    'label': 'Kostnadsreduksjon'},
                    {'num': '4 min',  'label': 'Cutover-vindu'},
                    {'num': '99,99%', 'label': 'Oppetids-SLA'},
                    {'num': '<60s',   'label': 'Testet RTO'},
                ],
                'tech': ['AWS', 'Terraform', 'RDS Aurora', 'CloudFront', 'Route 53', 'ECS Fargate', 'CDK'],
                'timeline': [
                    {'phase': '01', 'title': 'Arkitekturgjennomgang',   'desc': 'Kartla alle tjenester, avhengigheter og dataflyter. Identifiserte 3 enkeltfeilpunkter og 14 manuelt provisjonerte ressurser.'},
                    {'phase': '02', 'title': 'IaC og plan',             'desc': 'Kodifiserte all eksisterende infrastruktur i Terraform. Designet målarkitektur og trinnvis cutover-plan med automatiske tilbakerullingssteg.'},
                    {'phase': '03', 'title': 'Parallell bygging',       'desc': 'Provisjonerte replikaregionen parallelt med live produksjon — ingen driftsforstyrrelser under bygging. Kjørte 2× belastningstester.'},
                    {'phase': '04', 'title': 'Cutover uten nedetid',    'desc': 'Trafikk ble gradvis overført via vektet ruting over 15 minutter. DB-failover bekreftet under 60 sekunder RTO.'},
                ],
            },
            'analytics-pipeline': {
                'tag':      'Dataingeniørarbeid',
                'img':      'analytics.svg',
                'name':     'Sanntids analysepipeline',
                'subtitle': '5M+ daglige hendelser med forsinkelse under ett millisekund — live dashboards og automatiske varsler.',
                'overview': 'En nordisk e-handelsplattform erstattet nattlige batchrapporter med en sanntids strømmepipeline på Databricks. Produkt- og driftsteam ser nå live hendelsesdata innen sekunder.',
                'challenge': 'Eksisterende nattlige ETL-jobber gjorde bedriften blind for intra-dag trender. Teamene hadde ingen synlighet på live konverteringsrater eller lagerbeholdning før neste morgen — da var inntekter allerede tapt.',
                'solution': 'Vi bygde en strømmepipeline på Databricks med Delta Live Tables, som henter inn Kafka-hendelser fra 14 applikasjonstjenester i sanntid. Power BI kobles til via DirectQuery for live dashboardoppdateringer. Databricks SQL-varsler sender Slack- og e-postvarsler innen 30 sekunder ved terskelbrudd.',
                'outcome': 'Pipelinen behandler 5M+ hendelser per dag med forsinkelse under 1ms. Datateamets vedlikeholdsarbeid falt med 70%. Bedriften oppdaget og løste et betalingsgateway-problem innen 8 minutter.',
                'metrics': [
                    {'num': '5M+',  'label': 'Hendelser / dag'},
                    {'num': '<1ms', 'label': 'Gjennomsnittlig forsinkelse'},
                    {'num': '99,9%','label': 'Pipeline-SLA'},
                    {'num': '<30s', 'label': 'Varselrespons'},
                ],
                'tech': ['Databricks', 'Delta Live Tables', 'Apache Kafka', 'Python', 'Power BI', 'Azure', 'SQL', 'Spark'],
                'timeline': [
                    {'phase': '01', 'title': 'Dataoppdagelse',       'desc': 'Reviderte alle hendelseskilder, skjemakvalitet og volumemønstre på tvers av 14 applikasjonstjenester.'},
                    {'phase': '02', 'title': 'Pipelinarkitektur',    'desc': 'Designet strømmingstopologi med idempotente skriveroperasjoner, håndtering av sene ankomster og skjemaregister.'},
                    {'phase': '03', 'title': 'Bygg og belastningstest','desc': 'Distribuerte Delta Live Tables med enhetstestet transformasjonslogikk. Belastningstestet ved 2× toppvolum.'},
                    {'phase': '04', 'title': 'Dashboards og varsler', 'desc': 'Bygde 6 live Power BI-dashboards og konfigurerte terskelvarsler for 12 forretnings-KPI-er.'},
                ],
            },
            'zero-trust-auth': {
                'tag':      'Cybersikkerhet',
                'img':      'auth.svg',
                'name':     'Zero-trust autentisering',
                'subtitle': 'Felles identitet på tvers av tre enterprise-plattformer — OAuth 2.0, OIDC og detaljert RBAC.',
                'overview': 'Et finansforetak konsoliderte identitetshåndtering på tvers av tre interne plattformer i ett zero-trust autentiseringslag, etter at eksterne revisorer flagget arkitekturen som et kritisk kontrollsvikt.',
                'challenge': 'Tre applikasjoner hadde separate brukerlagre og øktshåndtering uten felles tilbakekallingskapabilitet. Tilbakekalling av en kompromittert konto krevde manuell handling i tre systemer — det tok opptil 30 minutter.',
                'solution': 'Vi distribuerte Keycloak som sentral IdP med OAuth 2.0 Authorization Code + PKCE-flyter og OIDC discovery-endepunkter. Hver plattform ble integrert via konfidensielle klienter med kortlevde JWTer (15 min TTL) og rotering av oppdateringstokens. RBAC-roller ble kartlagt fra Active Directory-gruppemedlemskap.',
                'outcome': 'Tilbakekalling av brukerrettigheter på tvers av alle systemer tar nå under 5 sekunder. Foretaket besto en ekstern penetrasjonstest uten kritiske funn og oppfylte alle krav fra compliance-revisorene.',
                'metrics': [
                    {'num': '3',    'label': 'Plattformer samlet'},
                    {'num': '<5s',  'label': 'Tilgangstilbakekalling'},
                    {'num': '100%', 'label': 'Revisjonsdekning'},
                    {'num': '0',    'label': 'Penetrasjonstestfunn'},
                ],
                'tech': ['Keycloak', 'OAuth 2.0', 'OIDC', 'JWT', 'RBAC', 'Active Directory', 'Python', 'Nginx'],
                'timeline': [
                    {'phase': '01', 'title': 'Sikkerhetsgjennomgang',  'desc': 'Kartla autentiseringsflyter på tvers av alle tre plattformer. Dokumenterte eskaleringsveier og revisjonsgap.'},
                    {'phase': '02', 'title': 'IdP-design',             'desc': 'Konfigurerte Keycloak realm, klientomfang, rollekartlegging og AD-federasjon med automatisk gruppesynkronisering.'},
                    {'phase': '03', 'title': 'Plattformintegrasjon',   'desc': 'Integrerte hver applikasjon via OIDC-mellomvare — minimale kodeendringer, bakoverkompatibel tokenvalidering.'},
                    {'phase': '04', 'title': 'Pentest og lansering',   'desc': 'Ekstern penetrasjonstest bestått uten kritiske funn. Trinnvis utrulling over to uker uten brukerpåvirkning.'},
                ],
            },
            'hr-portal': {
                'tag':      'Automatisering',
                'img':      'hr-portal.svg',
                'name':     'Power Platform HR-portal',
                'subtitle': 'Permisjonshåndtering automatisert — godkjenningstid redusert fra 3 dager til 4 timer, 60% mindre administrasjon.',
                'overview': 'Et norsk selskap med 500 ansatte erstattet e-postbasert HR-forespørselshåndtering med en selvbetjeningsportal på Power Apps, med automatiserte godkjenningsflyter i Power Automate.',
                'challenge': 'Manuell permisjonshåndtering krevde gjennomsnittlig 3–4 e-postkjeder og 3 virkedager per forespørsel. HR hadde ingen sanntidssynlighet på teamdekning. Månedlig lønnseksport var en fullstendig manuell 4-timers prosess.',
                'solution': 'Vi bygde en selvbetjenings-HR-portal på Power Apps koblet til SharePoint-lister for lagring og Dataverse for datamodellen. Power Automate driver flerstegs godkjenningsflyter: linjeleder → HR → lønnsmelding, med automatisk eskalering etter 48 timer. Portalen viser live teamkalendere, permisjonssaldoer og ett-klikks lønnseksport.',
                'outcome': 'Gjennomsnittlig godkjenningstid falt fra 3 dager til under 4 timer. HR-administrasjonsarbeidet ble redusert med 60%. Den månedlige lønnseksporten er fullt automatisert. Null lønningsfeil siden lansering.',
                'metrics': [
                    {'num': '3d→4t', 'label': 'Godkjenningstid'},
                    {'num': '60%',   'label': 'Spart administrasjonstid'},
                    {'num': '100%',  'label': 'Prosess automatisert'},
                    {'num': '0',     'label': 'Lønningsfeil'},
                ],
                'tech': ['Power Apps', 'Power Automate', 'SharePoint', 'Dataverse', 'Microsoft 365', 'Power BI'],
                'timeline': [
                    {'phase': '01', 'title': 'Prosesskartlegging',    'desc': 'Gjennomførte workshops med HR, ledere og lønn for å dokumentere hele forespørselslivssyklusen og beslutningsreglene.'},
                    {'phase': '02', 'title': 'Appdesign',             'desc': 'Designet skisser, datamodell i Dataverse og godkjenningslogikk. Godkjent av HR før bygging startet.'},
                    {'phase': '03', 'title': 'Bygg og automatiser',   'desc': 'Bygde Power App med 4 skjermer, Power Automate-flyter med eskalerings- og lønnskobling, og Power BI-dekningsdashboard.'},
                    {'phase': '04', 'title': 'Utrulling og opplæring','desc': 'Trinnvis utrulling til 3 pilotteam med raske tilbakemeldingssykluser, deretter selskapsdekkende utsendelse med opplæringsguider.'},
                ],
            },
        },
    },
}

def get_lang(request):
    lang = request.args.get('lang') or request.cookies.get('lang', 'en')
    return lang if lang in TRANSLATIONS else 'en'

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    lang = get_lang(request)
    t = TRANSLATIONS[lang]
    resp = render_template('index.html', t=t, lang=lang)
    from flask import make_response
    response = make_response(resp)
    response.set_cookie('lang', lang, max_age=60*60*24*365)
    return response

@app.route('/about')
def about():
    lang = get_lang(request)
    t = TRANSLATIONS[lang]
    return render_template('about.html', t=t, lang=lang)

@app.route('/contact')
def contact():
    lang = get_lang(request)
    t = TRANSLATIONS[lang]
    return render_template('contact.html', t=t, lang=lang)

@app.route('/case-study/<slug>')
def case_study(slug):
    lang = get_lang(request)
    t = TRANSLATIONS[lang]
    studies = t.get('case_studies', {})
    if slug not in studies:
        abort(404)
    study = studies[slug]
    return render_template('case_study.html', t=t, lang=lang, study=study, slug=slug)

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    company = data.get('company', '').strip()
    service = data.get('service', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'ok': False, 'error': 'Missing required fields'}), 400

    try:
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 0; }}
    .wrap {{ max-width: 580px; margin: 32px auto; background: #fff;
             border-radius: 8px; overflow: hidden;
             border: 1px solid #e2e8f0; }}
    .header {{ background: #0C1525; padding: 24px 32px; }}
    .header span {{ color: #2F6FEB; font-size: 22px; font-weight: 800;
                    letter-spacing: -0.5px; }}
    .header span em {{ color: #fff; font-style: normal; }}
    .badge {{ display: inline-block; background: rgba(47,111,235,0.12);
              color: #2F6FEB; border: 1px solid rgba(47,111,235,0.3);
              border-radius: 4px; font-size: 11px; letter-spacing: 0.1em;
              padding: 3px 10px; margin-top: 8px; text-transform: uppercase; }}
    .body {{ padding: 28px 32px; }}
    .row {{ margin-bottom: 16px; }}
    .label {{ font-size: 11px; color: #94a3b8; text-transform: uppercase;
              letter-spacing: 0.08em; margin-bottom: 3px; }}
    .value {{ font-size: 15px; color: #1e293b; font-weight: 500; }}
    .message-box {{ background: #f8fafc; border: 1px solid #e2e8f0;
                    border-radius: 6px; padding: 16px; margin-top: 20px; }}
    .message-box .label {{ margin-bottom: 8px; }}
    .message-box p {{ font-size: 14px; color: #334155; line-height: 1.7; margin: 0; }}
    .footer {{ background: #f8fafc; border-top: 1px solid #e2e8f0;
               padding: 14px 32px; font-size: 11px; color: #94a3b8; }}
    .reply-btn {{ display: inline-block; margin-top: 20px; background: #2F6FEB;
                  color: #fff; padding: 10px 22px; border-radius: 6px;
                  text-decoration: none; font-size: 13px; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <span><em>Cry</em>ton</span><br/>
      <span class="badge">New inquiry</span>
    </div>
    <div class="body">
      <div class="row">
        <div class="label">Name</div>
        <div class="value">{name}</div>
      </div>
      <div class="row">
        <div class="label">Email</div>
        <div class="value"><a href="mailto:{email}" style="color:#2F6FEB;">{email}</a></div>
      </div>
      {"<div class='row'><div class='label'>Company</div><div class='value'>" + company + "</div></div>" if company else ""}
      {"<div class='row'><div class='label'>Service of interest</div><div class='value'>" + service + "</div></div>" if service else ""}
      <div class="message-box">
        <div class="label">Message</div>
        <p>{message.replace(chr(10), '<br/>')}</p>
      </div>
      <a href="mailto:{email}?subject=Re: Your inquiry to Cryton" class="reply-btn">
        Reply to {name} →
      </a>
    </div>
    <div class="footer">
      Sent via cryton.no contact form · Cryton · Oslo, Norway
    </div>
  </div>
</body>
</html>"""

        send_email(
            to=os.getenv('CONTACT_RECIPIENT', ''),
            reply_to=email,
            subject=f'[Cryton] New inquiry from {name}',
            html_body=html_body,
        )
        return jsonify({'ok': True})
    except Exception as e:
        app.logger.error(f'Mail error [{type(e).__name__}]: {e}')
        return jsonify({'ok': False, 'error': 'Failed to send message. Please try again.'}), 500

@app.route('/api/health')
def health():
    username = app.config.get('MAIL_USERNAME', '')
    return jsonify({
        'mail_server':    app.config.get('MAIL_SERVER'),
        'mail_port':      app.config.get('MAIL_PORT'),
        'mail_username':  username[:6] + '***' if username else 'NOT SET',
        'mail_password':  'SET' if app.config.get('MAIL_PASSWORD') else 'NOT SET',
        'recipient':      'SET' if os.getenv('CONTACT_RECIPIENT') else 'NOT SET',
        'secret_key':     'SET' if app.config.get('SECRET_KEY') != 'dev-secret-change-in-production' else 'DEFAULT (change this)',
    })

@app.route('/api/lang/<code>')
def set_lang(code):
    if code not in TRANSLATIONS:
        code = 'en'
    from flask import make_response
    response = make_response(jsonify({'ok': True, 'lang': code}))
    response.set_cookie('lang', code, max_age=60*60*24*365)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
