# 🧠 Multi-Tool Chatbot  
**(Chainlit + TogetherAI + OpenRouter + Gemini)**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Chainlit](https://img.shields.io/badge/Built%20With-Chainlit-FF5F00)](https://www.chainlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

An advanced, modular AI assistant built with [Chainlit](https://www.chainlit.io/), integrated with multiple LLM providers like **Gemini**, **TogetherAI**, and **OpenRouter**, and powered by a suite of useful tools for enhanced user interaction.

---

## ✨ Key Features

- ✅ **Multi-LLM Support** – Gemini, Together Meta, Exaone, OpenRouter DeepSeek  
- 🔧 **Tool-Based Modular Architecture** – Easy integration via `function_tool`  
- 🧠 **Dynamic Model Configuration** – Switch profiles on the fly  
- 💬 **Live Typing & Streamed Responses** – Real-time interaction  
- 🧾 **Persistent Chat History** – Auto-saves to JSON  
- 🎯 **Starter Prompts** – For better user engagement

---

## 🧰 Built-in Tools

- 🌦️ **Weather Checker**  
- 🗞️ **News Fetcher**  
- 😂 **Programming Joke Teller**  
- 💱 **Currency Exchange Lookup**  
- ✍️ **EasyWriter** – Writing assistant  
- 📧 **EmailWriter** – Email generator  
- 🌏 **Language Translator**  
- 🧪 **Prompt Engineer**
- 🌐 **IP Geolocation**
- 🪲 **Code Debugger** - Debug and improve code


---

## 📁 Project Structure


├── main.py # Entry point with chat logic, streaming, and tools
├── my_secrets.py # Handles environment variables securely
├── .env # API keys and config (not committed)
├──images #contain output and interface images
├──public #contain svg logos for starter tools
└── chat_history.json # Chat history output file (on session end)

## 📬 Contact

For questions, reach out via GitHub Issues or [muhammadusman5965etc@gmail.com](mailto:muhammadusman5965etc@gmail.com)

## 🚆Interface Preview

![Interface](/images/Interface.png)

## 📤Sample Output

![Output](/images/Output.png)
