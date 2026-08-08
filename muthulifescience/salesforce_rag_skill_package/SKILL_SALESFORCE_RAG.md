# ⚡ STANDALONE SALESFORCE RAG & AI AGENT SKILL SPECIFICATION

**Skill Name:** `salesforce-architect-and-developer-rag`  
**Version:** `1.0.0`  
**Description:** Standalone RAG Knowledge Engine & Agent Skill for Salesforce (Apex, LWC, SF CLI, Health Cloud, Life Sciences Cloud, MuleSoft Direct, Data Cloud, OmniStudio, and Agentforce AI).  
**Target RAG Frameworks:** OpenAI Custom GPTs, Claude Projects, LangChain, LlamaIndex, Pinecone, ChromaDB, AutoGen, CrewAI, and Custom LLM Pipelines.

---

## 🎯 SECTION 1: AGENT IDENTITY & CORE INSTRUCTIONS (SYSTEM PROMPT)

```markdown
You are an Expert Salesforce Solutions Architect and Technical Lead. 

### Core Operating Principles:
1. **Salesforce Platform Standards:** Write clean, modular, bulkified Apex code adhering to enterprise design patterns (Selector, Service, Domain layer). Always enforce FLS/CRUD security (`WITH USER_MODE` or `Security.stripInaccessible()`).
2. **Lightning Web Components (LWC):** Use SLDS design tokens, reactive properties (`@wire`), async/await Apex calls, and clean event handling. Avoid hardcoded pixel widths and direct DOM mutation.
3. **SF CLI Execution:** Generate precise `sf data query`, `sf data create`, `sf project deploy` commands with explicit `--target-org` flags.
4. **Health Cloud & Life Sciences Cloud (LSC):** Model Patients as Person Accounts, HCPs as HealthcareProviders with NPI validation, and HCOs as HealthcareFacilities. Enforce FDA 21 CFR Part 11 Chain of Custody, Sunshine Act compliance, and MIR off-label escalation firewalls (`IsEscalated = true`).
5. **Interoperability (MuleSoft & FHIR R4):** Transform raw SQL / FHIR R4 JSON payloads to `CareObservation` and `ClinicalEncounter` SObjects using DataWeave 2.0.
6. **Agentforce AI & Data Cloud:** Enforce HIPAA guardrails, Grounded Prompt Templates, and Data Cloud Zero-Copy SQL federation.
```

---

## 📚 SECTION 2: CURATED RAG KNOWLEDGE BASE INDEX (DATA SOURCES)

To ingest this RAG skill into any Vector Database or Agent Framework, chunk and index the following 6 core knowledge modules:

### 📄 Module 1: Salesforce Core Architecture (`01_salesforce_core_rag.md`)
* Apex enterprise patterns (Selector, Service, Domain layers).
* SOQL query optimization, governor limits, bulkification, batchable/queueable Apex.
* LWC state management, SLDS styling tokens, wire adapters, and PubSub events.
* SF CLI metadata deployment, org authorization, and data scripting.

### 📄 Module 2: Health Cloud & Life Sciences Cloud Schema (`02_lifesciences_schema_rag.md`)
* Person Accounts vs Provider Accounts (`HealthcareProvider`, `HealthcareFacility`, `NPI`).
* Patient Support Programs (`CareProgramEnrollee`, `CareProgram`, `CoverageBenefit`).
* Clinical Trial Operations (`ResearchStudy`, `ResearchStudyCandidate`).
* MedTech Surgical Case Planning & UDI Tracking (`Asset`, `WorkOrder`).

### 📄 Module 3: Advanced Therapy Management (ATM) & Chain of Custody (`03_atm_chain_of_custody_rag.md`)
* 3-Stage Vein-to-Vein slot scheduling for CAR-T cell therapies (`WorkOrder`, `CustodyItem`).
* FDA 21 CFR Part 11 digital signatures (`DigitalSignature`) & barcode logging (`BATCH-CAR-T-2026-9901`).

### 📄 Module 4: MuleSoft Direct & HL7 FHIR R4 Interoperability (`04_mulesoft_fhir_rag.md`)
* HL7 FHIR R4 JSON mapping matrix to Salesforce `CareObservation` and `ClinicalEncounter`.
* MuleSoft DataWeave 2.0 scripts & XML flows (`<scheduler>`, `<db:select>`, `<salesforce:create>`, `<db:update>`).
* Incremental state pipeline (`sync_status = 'NEW'` $\rightarrow$ `'PROCESSED'`).

### 📄 Module 5: OmniStudio & Flow Orchestrator (`05_omnistudio_orchestrator_rag.md`)
* OmniScripts, FlexCards, Integration Procedures (IPs), and DataRaptors (Turbo Extract / Transform).
* Flow Orchestrator multi-stage approval processes (`ApprovalWorkItem`).

### 📄 Module 6: Agentforce AI & Data Cloud Zero-Copy (`06_agentforce_datacloud_rag.md`)
* Agentforce AI Autonomous Health Bots, 24/7 prescription refill handling (`Case`).
* Grounded Prompt Builder Templates (`DOSSIER-ONCO-2026`).
* Data Cloud Zero-Copy SQL federation against Snowflake / Databricks data lakes.

---

## 🛠️ SECTION 3: RAG VECTOR DATABASE INGESTION GUIDE

### 🐍 LangChain Python RAG Ingestion Example:

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load Knowledge Base Documents
loader = DirectoryLoader('./salesforce_rag_knowledge_base', glob="*.md", loader_cls=TextLoader)
documents = loader.load()

# 2. Chunk Documents for Vector Indexing
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(documents)

# 3. Create Vector Store (ChromaDB)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma.from_documents(chunks, embeddings, persist_directory="./salesforce_rag_vector_db")

print("Successfully indexed Salesforce RAG Knowledge Base!")
```

### 🤖 OpenAI Custom GPT / Claude Project Setup:
1. Create a new Custom GPT or Claude Project named **Salesforce Architect & Developer RAG**.
2. Copy **Section 1 (System Prompt)** into the Instructions text box.
3. Upload the files in `salesforce_rag_knowledge_base/` under **Knowledge / Knowledge Base Files**.
4. Enable **Code Interpreter** and **File Search / Web Search**.

---

## 🚀 SECTION 4: HOW TO USE THIS STANDALONE SKILL

This skill can now run independently in:
* **Custom AI Agents** (CrewAI, AutoGen, LangGraph)
* **VS Code AI Extensions** (Cursor, Continue.dev, Copilot Workspace)
* **Enterprise LLM Apps** (OpenAI ChatGPT Enterprise, Claude for Work, Ollama local LLMs)
