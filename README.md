# 📧 AI Email Generator with Conversational Memory

An AI-powered email generation application built using **Python, LangChain, OpenAI, and JSON-based persistent memory**.

The application generates professional emails based on user-provided context and writing tone. It also stores previous email requests and generated emails in a JSON file, allowing relevant information from earlier interactions to be supplied to the language model when generating subsequent emails.

This project demonstrates how to build an LLM-powered application with prompt engineering, LangChain Expression Language (LCEL), command-line argument parsing, and persistent conversational context.

---

## 🎯 Project Objectives

The primary objectives of this project are to:

* Generate complete emails using an OpenAI language model.
* Support formal, informal, and neutral writing tones.
* Build reusable prompts using LangChain `PromptTemplate`.
* Connect prompts and language models using LCEL.
* Store previous email interactions in `memory.json`.
* Load conversation history across application restarts.
* Pass relevant historical context to the LLM.
* Manage API credentials securely using environment variables.
* Implement a command-line interface using Python's `argparse`.

---

## ✨ Key Features

### 1. AI-Powered Email Generation

Generates complete emails containing:

* Subject line
* Greeting
* Email body
* Appropriate sign-off

### 2. Multiple Writing Tones

The application supports three writing styles:

| Tone       | Description                 | Example Use Case                                                |
| ---------- | --------------------------- | --------------------------------------------------------------- |
| `formal`   | Professional and structured | Business communication, leave requests, official correspondence |
| `informal` | Casual and friendly         | Messages to friends and familiar colleagues                     |
| `neutral`  | Clear and balanced          | General workplace communication                                 |

### 3. Conversational Memory

The application stores previous email interactions in `memory.json`.

Each interaction contains:

* Email context
* Requested tone
* Generated email

Previously saved interactions are loaded when the application starts.

### 4. Persistent Storage

Conversation history survives application restarts because it is saved to a local JSON file.

### 5. Context-Aware Generation

Previous interactions are formatted and passed to the LLM alongside the current email request.

The model can reuse relevant details from earlier requests, subject to the instructions in the prompt.

### 6. Command-Line Interface

Users can generate emails directly from the terminal by supplying the email context and desired tone.

### 7. Error Handling

The application validates input, checks for the OpenAI API key, and reports common configuration and API errors.

---

## 🛠️ Technology Stack

| Technology         | Purpose                                  |
| ------------------ | ---------------------------------------- |
| Python             | Application logic                        |
| OpenAI GPT-4o-mini | Email generation                         |
| LangChain          | LLM integration and prompt orchestration |
| `langchain-openai` | OpenAI chat model integration            |
| `langchain-core`   | `PromptTemplate` and LCEL                |
| `python-dotenv`    | Environment variable management          |
| JSON               | Persistent conversation storage          |
| `argparse`         | Command-line argument parsing            |
| `pathlib`          | Cross-platform file path management      |

---

## 🏗️ System Architecture

The application follows a straightforward LLM processing pipeline.

```text
                 ┌──────────────────────┐
                 │     User Input       │
                 │  Context + Tone      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     main()           │
                 │  Parse CLI Arguments │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    load_memory()     │
                 │  Read memory.json    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   format_memory()    │
                 │ Format Previous Data │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   PromptTemplate     │
                 │ History + Context    │
                 │       + Tone         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    LCEL Pipeline     │
                 │     prompt | llm     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   OpenAI LLM         │
                 │   GPT-4o-mini        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Generated Email      │
                 │   result.content     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    save_memory()     │
                 │ Update memory.json   │
                 └──────────────────────┘
```

### Workflow Explanation

1. The user provides an email context and writing tone.
2. The application parses the command-line arguments.
3. `load_memory()` retrieves previously saved email interactions.
4. `format_memory()` converts the saved interactions into readable text.
5. `PromptTemplate` combines the history, current context, and requested tone.
6. The LCEL pipeline sends the prompt to the OpenAI model.
7. The generated email is displayed in the terminal.
8. The current request and generated email are added to memory.
9. `save_memory()` persists the updated history in `memory.json`.

**Important:** The LLM itself does not automatically remember earlier API calls. The application supplies previous interactions in the prompt.

---

## 📂 Project Structure

```text
AI-Email-Generator/
│
├── main.py
│   └── Main application and email-generation logic
│
├── memory.json
│   └── Persistent email conversation history
│
├── .env
│   └── OpenAI API key
│
├── .env.example
│   └── Example environment configuration
│
├── .gitignore
│   └── Files excluded from Git tracking
│
├── requirements.txt
│   └── Python dependencies
│
└── README.md
    └── Project documentation
```

**Note:** `memory.json` is created automatically after the first successful email generation and save operation. The `.env` file must be configured locally.

---

## ⚙️ Prerequisites

Before running the project, ensure you have:

* Python 3.10 or later.
* An OpenAI API key.
* An active internet connection.
* Visual Studio Code or another Python editor.
* Git, if you plan to clone or publish the project.
* API access and sufficient quota for the selected model.

API usage may incur charges depending on your account and usage.

---

## 🚀 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

Navigate to the project directory:

```bash
cd AI-Email-Generator
```

Replace `<your-github-repository-url>` with your actual repository URL.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Alternatively, activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

### Step 3: Create `requirements.txt`

Add the following dependencies:

```text
langchain-core
langchain-openai
python-dotenv
```

Install them:

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure the OpenAI API Key

Create a `.env` file in the project root.

Add:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your actual API key.

Do not share your key or commit the `.env` file to GitHub.

### Step 5: Create `.gitignore`

Add:

```gitignore
# API credentials
.env
.env.*

# Allow a safe example configuration
!.env.example

# Virtual environments
.venv/
venv/

# Python cache
__pycache__/
*.py[cod]

# Jupyter checkpoints
.ipynb_checkpoints/

# Local conversation history
memory.json
```

This prevents API credentials and local conversation history from being accidentally committed.

### Step 6: Create `.env.example`

For repository documentation, create an `.env.example` file containing:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

This is a template only. Users must supply their own API key.

---

## ▶️ Running the Application

Make sure your virtual environment is activated and your `.env` file is configured.

Run:

```bash
python main.py --context "Schedule a project kickoff meeting" --tone formal
```

The application should display the number of previous interactions loaded, generate an email, and save the interaction.

Example terminal output:

```text
Previous interactions loaded: 0

Generating a formal email...

============================================================

Subject: Project Kickoff Meeting

Dear [Recipient Name],

I would like to schedule a project kickoff meeting to
discuss the project objectives, scope, responsibilities,
and upcoming milestones.

Please let me know your availability so that we can
finalize a suitable meeting time.

Best regards,
[Your Name]

============================================================
Email generated successfully!
Conversation saved to: .../memory.json
```

The generated email is illustrative; actual output will vary.

---

## 💬 Usage Examples

### 1. Generate a Formal Email

```bash
python main.py --context "Request a meeting with my manager" --tone formal
```

### 2. Generate an Informal Email

```bash
python main.py --context "Invite my friend for lunch this weekend" --tone informal
```

### 3. Generate a Neutral Email

```bash
python main.py --context "Inform the team about a deadline change" --tone neutral
```

### 4. Use the Default Tone

```bash
python main.py --context "Thank a colleague for helping with a project"
```

The default tone is `neutral`.

### 5. Display Help

```bash
python main.py --help
```

This displays the supported arguments and usage examples.

---

## 🧠 Conversational Memory in Action

This project uses JSON-based persistence to store previous email requests and their generated responses.

### First Interaction

Run:

```bash
python main.py --context "Write an email to my manager Ramesh requesting leave next Monday" --tone formal
```

The application generates an email and saves the interaction.

### Second Interaction

Run:

```bash
python main.py --context "Write a follow-up email asking whether my leave request has been approved" --tone formal
```

The application loads the previous interaction and includes it in the new prompt.

The LLM can use relevant details from the earlier request, such as the manager's name and the leave date.

### Restart the Application

Close the terminal and run another command.

The application reads the saved history from `memory.json`, allowing previous interactions to be reused across application runs.

**Limitation:** The model receives previous history as text. It may not always recall details perfectly, and it does not independently verify whether historical information remains accurate.

---

## 🗃️ Understanding `memory.json`

The file stores each successful interaction as a JSON object.

Example:

```json
[
  {
    "context": "Write an email to my manager Ramesh requesting leave next Monday",
    "tone": "formal",
    "email": "Subject: Leave Request for Next Monday\n\nDear Ramesh,\n\nI would like to request leave..."
  },
  {
    "context": "Write a follow-up email asking whether my leave request has been approved",
    "tone": "formal",
    "email": "Subject: Follow-Up on Leave Request\n\nDear Ramesh,\n\nI am writing to follow up..."
  }
]
```

### Memory Functions

| Function                | Responsibility                                      |
| ----------------------- | --------------------------------------------------- |
| `load_memory()`         | Reads previous interactions from JSON               |
| `save_memory(memory)`   | Writes updated interactions to JSON                 |
| `format_memory(memory)` | Converts saved interactions into readable text      |
| `generate_email()`      | Generates an email using context, tone, and history |
| `main()`                | Coordinates input, generation, and persistence      |

### Where Is the Memory File Stored?

The application uses `pathlib` to define the file location relative to `main.py`.

Consequently, `memory.json` is stored in the project directory, rather than whichever directory happens to be the terminal's current working directory.

---

## 🔍 Core Implementation Concepts

### 1. PromptTemplate

`PromptTemplate` defines the instructions and variables supplied to the LLM.

```python
prompt = PromptTemplate.from_template(
    """
    Previous history:
    {history}

    Email context:
    {context}

    Requested tone:
    {tone}
    """
)
```

The template has three variables:

* `history`
* `context`
* `tone`

### 2. LangChain Expression Language (LCEL)

The following statement connects the prompt to the model:

```python
chain = prompt | llm
```

This creates a processing pipeline.

### 3. Model Invocation

```python
result = chain.invoke({
    "history": history,
    "context": context.strip(),
    "tone": tone
})
```

The model receives the previous history and current request.

### 4. Extracting the Response

```python
return result.content
```

For a standard `ChatOpenAI` pipeline, `result` is an AI message object and `.content` contains its generated response.

### 5. Persistent Memory

```python
memory.append({
    "context": args.context,
    "tone": args.tone,
    "email": email
})

save_memory(memory)
```

This stores the current request and generated email for future use.

---

## ⚠️ Limitations

The project is intended as a learning application and has several limitations.

* **Growing history:** All saved interactions are passed into the prompt, potentially increasing token usage and latency.
* **No automatic summarization:** Older conversations are not summarized.
* **No user isolation:** A single JSON file stores all interactions for this local application.
* **No interactive follow-up loop:** Each request is supplied through command-line arguments.
* **No database:** JSON is not ideal for concurrent access or multi-user production applications.
* **No guaranteed factual recall:** The model can misinterpret historical details.
* **No GUI:** The application currently runs in a terminal.
* **API dependency:** Successful generation requires a valid API key, network access, model availability, and sufficient quota.

---

## 🔮 Future Enhancements

Potential improvements include:

1. Add an interactive chat loop for follow-up instructions such as "make it shorter" or "change the tone."
2. Implement a sliding window to limit the amount of history sent to the model.
3. Summarize older interactions to reduce token usage.
4. Add user-specific memory.
5. Store conversations in SQLite or PostgreSQL.
6. Build a Streamlit web interface.
7. Develop a FastAPI backend.
8. Add automated tests using `pytest`.
9. Add logging and improved API error handling.
10. Support exporting generated emails to `.txt` or `.eml` files.

---

## 🧪 Troubleshooting

| Error                           | Possible cause                                         | Solution                                                         |
| ------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- |
| `ModuleNotFoundError`           | Dependencies are missing                               | Activate the virtual environment and install `requirements.txt`. |
| Missing API key                 | `.env` is absent or incorrectly configured             | Verify `OPENAI_API_KEY` and reload environment variables.        |
| `AuthenticationError`           | Invalid or revoked API key                             | Verify the key in your OpenAI API account.                       |
| `model_not_found`               | Incorrect model identifier or unavailable model access | Check the model name and API project permissions.                |
| `RateLimitError`                | Rate limit or quota issue                              | Check usage limits, billing, and retry timing.                   |
| `JSONDecodeError`               | Invalid JSON in `memory.json`                          | Restore valid JSON from a backup or reset disposable history.    |
| Empty conversation history      | No previous successful interactions                    | Generate and save an email first.                                |
| Previous details are not reused | History is missing, irrelevant, or too large           | Inspect `memory.json` and the formatted prompt history.          |

### Reset Conversation Memory

If you want to start with an empty history, back up any useful data and replace the contents of `memory.json` with:

```json
[]
```

Alternatively, delete the file. The application will create a new one after the next successful generation.

---

## 🔐 Security Considerations

* Never commit `.env` or API credentials.
* Keep `memory.json` out of public repositories when it contains personal or business information.
* Avoid storing sensitive information unnecessarily.
* Use proper secret management for cloud deployments.
* Consider access controls and encryption when introducing database-backed memory.
* Remember that conversation history is included in prompts sent to the LLM provider.

---

## 📚 Learning Outcomes

By completing this project, you will gain practical experience with:

* Python application development.
* OpenAI API integration.
* LangChain prompt engineering.
* LangChain Expression Language.
* Context-aware LLM generation.
* JSON serialization and persistent storage.
* Environment variable management.
* Command-line argument parsing.
* Error handling.
* Basic conversational memory architecture.

---

## 👨‍💻 Author

**AV Rajanna**

GitHub: Add your GitHub profile URL here.

LinkedIn: Add your LinkedIn profile URL here.

---

## 📄 License

This project was developed for educational purposes.

If you intend to distribute it as an open-source project, consider adding an appropriate license, such as the MIT License.
