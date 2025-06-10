import json
from typing import cast

import chainlit as cl
import requests
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    set_default_openai_client,
    set_tracing_disabled,
)
from openai.types.responses import ResponseTextDeltaEvent

from my_secrets import Secrets

secrets = Secrets()


# created a tool to get the current weather using external api
@function_tool("current_weather_tool")
@cl.step(type="weather tool")
def current_weather_tool(location: str) -> str:
    """
    This function makes a request to a weather API and returns formatted weather
    information including temperature, conditions, wind, humidity, and UV index.

    Args:
        location (str): The location to get weather for (city name)

    Returns:
        str: A formatted string containing current weather information if successful,
             or an error message if the API request fails
    """

    result = requests.get(
        f"{secrets.weather_base_url}/current.json?key={secrets.weather_api_key}&q={location}"
    )
    if result.status_code == 200:
        data = result.json()
        return f"Current weather in {data['location']['name']}, {data['location']['region']}, {data['location']['country']} as of {data['location']['localtime']} is {data['current']['temp_c']}°C ({data['current']['condition']['text']}), feels like {data['current']['feelslike_c']}°C, wind {data['current']['wind_kph']} km/h {data['current']['wind_dir']}, humidity {data['current']['humidity']}% and UV index is {data['current']['uv']}."
    else:
        return "Sorry, I couldn't fetch the weather data. Please try again later"


# created a tool to get the recent news update about any topic
@function_tool("news_update")
@cl.step(type="Recent News Update")
def news_update(topic: str) -> str:
    """
    Fetches the latest news headlines on a given topic using a news API.

    Args:
        topic (str): The keyword or topic to search news for.

    Returns:
        str: A formatted list of the top 3 news headlines, or an error message.
    """
    result = requests.get(
        f"{secrets.news_base_url}?q={topic}&apiKey={secrets.news_api_key}&pageSize=3&sortBy=publishedAt"
    )
    if result.status_code == 200:
        data = result.json()
        articles = data.get("articles", [])
        if not articles:
            return f"Sorry, no recent news found on '{topic}'."
        response = f"Here are the top {len(articles)} news headlines on '{topic}':\n"
        for i, article in enumerate(articles, 1):
            response += (
                f"{i}. {article['title']} (Source: {article['source']['name']})\n"
            )
        return response.strip()
    else:
        return "Sorry, I couldn't fetch the news at the moment. Please try again later."


# created a random joke teller tool
@function_tool("joke_teller_tool")
@cl.step(type="Joke Tool")
def joke_teller_tool() -> str:
    """
    Fetches a random joke (single-line or two-part) from a joke API.

    Returns:
        str: The joke if successful, or an error message if the request fails.
    """
    url = f"{secrets.joke_api_base_url}?type=single,twopart"
    result = requests.get(url)
    if result.status_code == 200:
        data = result.json()
        if data["type"] == "single":
            return data["joke"]
        elif data["type"] == "twopart":
            return f"{data['setup']}\n{data['delivery']}"
        else:
            return "Hmm, couldn't find a joke this time. Try again!"
    else:
        return "Sorry, I couldn't fetch a joke right now. Please try again later."


# created a tool to get the current currency exchange rate for any currency
@function_tool("currency_exchange_tool")
@cl.step(type="Currency Exchange Tool")
def currency_exchange_tool(base_currency: str, target_currency: str) -> str:
    """
    Fetches the latest currency exchange rate between two currencies.

    Args:
        base_currency (str): Currency code to convert from (e.g., 'USD').
        target_currency (str): Currency code to convert to (e.g., 'EUR').

    Returns:
        str: The formatted exchange rate if available, or an error message.
    """
    url = f"{secrets.currency_exchange_base_url}/{secrets.currency_exchange_api_key}/latest/{base_currency.upper()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("result") == "success":
            rates = data.get("conversion_rates", {})
            rate = rates.get(target_currency.upper())
            if rate:
                return f"Exchange rate from {base_currency.upper()} to {target_currency.upper()} is {rate:.4f}."
            else:
                return f"Sorry, I couldn't find the exchange rate for '{target_currency.upper()}'. Please check the currency code."
        else:
            return "Sorry, the API did not return a successful result."
    else:
        return "Sorry, I couldn't fetch currency exchange data right now. Please try again later."


# added starter for all the tools to make the use of tools fast
@cl.set_starters
async def starter():
    return [
        cl.Starter(
            label="Check Weather",
            message="Fetch the current weather for a specified location.",
            icon="/public/weather-news.svg",
        ),
        cl.Starter(
            label="Latest News",
            message="Stay updated—fetch the latest news on any topic of your choice.",
            icon="/public/megaphone.svg",
        ),
        cl.Starter(
            label="Tell me a joke",
            message="Can you tell me a funny joke?",
            icon="/public/joking.svg",
        ),
        cl.Starter(
            label="Currency Exchange",
            message="Fetch the current exchange rate for any currency?",
            icon="/public/exchange-rate.svg",
        ),
        cl.Starter(
            label="EasyWriter",
            message="Can you help me write an easy and clear article about any topic?",
            icon="/public/easy.svg",
        ),
        cl.Starter(
            label="EmailWriter",
            message="Can you help me write an email for any topic?",
            icon="/public/up-arrow.svg",
        ),
        cl.Starter(
            label="LanguageTranslator",
            message="Translate any language into desired one.",
            icon="/public/languages.svg",
        ),
        cl.Starter(
            label="PromptEngineer",
            message="Help Me Write a Better Prompt",
            icon="/public/engine.svg"
        )
    ]


# Added chat profile to switch between different models
@cl.set_chat_profiles
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Gemini-2.0-flash",
            markdown_description="The underlying LLM model is **Gemini-2.0-flash**.",
            icon="/public/artificial-intelligence.svg",
        ),
        cl.ChatProfile(
            name="Meta-Llama-32b",
            markdown_description="The underlying LLM model is **Meta-Llama-32b**.",
            icon="/public/llama.svg",
        ),
        cl.ChatProfile(
            name="EXAONE-3.5-32b",
            markdown_description="The underlying LLM model is **EXAONE-3.5-32b**.",
            icon="/public/data-modelling.svg",
        ),
        cl.ChatProfile(
            name="DeepSeek-Chat-V3",
            markdown_description="The underlying LLM model is **DeepSeek-Chat-V3**.",
            icon="/public/whale.svg"
        ),
    ]

#on_chat_start from chainlit to load the things which are necessary to load at start to every chat
@cl.on_chat_start
async def start():
    secrets = Secrets()
    profile = cl.user_session.get("chat_profile") or {}
    selected_model = profile if profile else "Gemini-2.0-flash"

    # created model selection using if-else
    if selected_model == "Gemini-2.0-flash":
        external_client = AsyncOpenAI(
            base_url=secrets.gemini_base_url,
            api_key=secrets.gemini_api_key,
        )
        model_name = secrets.gemini_api_model

    elif selected_model == "Meta-Llama-32b":
        external_client = AsyncOpenAI(
            base_url=secrets.together_base_url,
            api_key=secrets.together_api_key,
        )
        model_name = secrets.together_model

    elif selected_model == "EXAONE-3.5-32b":
        external_client = AsyncOpenAI(
            base_url=secrets.together_base_url,
            api_key=secrets.together_api_key,
        )
        model_name = secrets.together_model1

    elif selected_model == "DeepSeek-Chat-V3":
        external_client = AsyncOpenAI(
            base_url=secrets.openrouter_base_url,
            api_key=secrets.openrouter_api_key,
        )
        model_name = secrets.openrouter_model
    else:
        external_client = AsyncOpenAI(
            base_url=secrets.gemini_base_url,
            api_key=secrets.gemini_api_key,
        )
        model_name = secrets.gemini_api_model

    set_tracing_disabled(True)
    set_default_openai_client(external_client)

    # created agents which can be used as tools
    easy_writer_agent = Agent(
        name="EasyWriter",
        instructions="You can write easy by the requirements and given topic by user.",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=model_name,
        ),
    )

    email_writer_agent = Agent(
        name="EmailWriter",
        instructions="""Compose well-structured emails from user inputs. 
                    Adjust tone (formal/informal), add a subject line, and 
                    end with a custom sign-off.""",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=model_name,
        ),
    )

    language_translator = Agent(
        name="LanguageTranslator",
        instructions="""
                Translate text from one language to another while preserving meaning, tone, and context.

                Args:
                    text (str): The text to be translated.
                    source_language (str): The language the original text is written in (e.g., "English", "en").
                    target_language (str): The language to translate the text into (e.g., "Spanish", "es").

                Returns:
                    str: The translated version of the input text in the target language.

                Notes:
                    - Maintain cultural and contextual accuracy.
                    - Translate idioms or expressions naturally where possible.
                    - Use formal or informal tone appropriately based on the source.
                    - If source_language is unknown, attempt to detect it.
                """,
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=model_name,
        ),
    )

    prompt_engineer_agent=Agent(
        name="PromptEngineer",
        instructions="""You are a senior prompt engineer with over a decade of experience in designing 
                    highly effective prompts for language models like GPT-4. Given any topic, your task 
                    is to craft the most clear, effective, and optimized prompt that will produce high-quality 
                    results from the model. Ask clarifying questions if needed.""",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=model_name,
        ),
    )

    #main agent to run all tools and agents which will run as-tool
    agent = Agent(
        name="Chatbot",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=model_name,
        ),
        # added tools in main agent to make them implemented
        tools=[
            current_weather_tool,
            currency_exchange_tool,
            news_update,
            joke_teller_tool,
            easy_writer_agent.as_tool(
                tool_name="EasyWriter",
                tool_description="You can write easy by the requirements and given topic by user.",
            ),
            email_writer_agent.as_tool(
                tool_name="EmailWriter",
                tool_description="Write easy-to-understand content based on the topic and instructions provided by the user.",
            ),
            language_translator.as_tool(
                tool_name="LanguageTranslator",
                tool_description="Translate any language into the desired language of the user.",
            ),
            prompt_engineer_agent.as_tool(
                tool_name="PromptEngineer",
                tool_description="a sineor prompt engineer with an experience of over a decade and give the most suitable prompt to the topic which user wants.",
            ),
        ],
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])
    cl.user_session.set("selected_model", selected_model)


@cl.on_message
async def main(message: cl.Message):
    selected_model = cl.user_session.get("selected_model") or "Gemini-2.0-flash"
    # added a generating respond message while the response is being generated by the model
    thinking_msg = cl.Message(content=f"🤖 {selected_model} is thinking...")
    await thinking_msg.send()

    agent = cast(Agent, cl.user_session.get("agent"))
    chat_history:list = cl.user_session.get("chat_history") or []

    #added user prompt to history
    chat_history.append({
        "role": "user",
        "content": message.content
        })
#added try-except for proper error handling
    try:
        # running the agent using the Runner class from openai
        result = Runner.run_streamed(
            starting_agent=agent,
            input=chat_history,
        )

        response_message = cl.Message(content="")
        first_response = True

        # for loop to convert model response into chunks and then stream it
        async for chunk in result.stream_events():
            if chunk.type == "raw_response_event" and isinstance(
                chunk.data, ResponseTextDeltaEvent
            ):
                if first_response:
                    await thinking_msg.remove()
                    await response_message.send()
                    first_response = False
                await response_message.stream_token(chunk.data.delta)

#added model response in history
        chat_history.append({
            "role": "assistant", 
            "content": response_message.content
            })
        
        cl.user_session.set("chat_history", chat_history)
        await response_message.update()

    except Exception as e:
        await thinking_msg.remove()
        error_msg = cl.Message(content="An error occurred. Please try again.")
        await error_msg.send()
        print(f"Error: {e}")

@cl.on_chat_end
def end():
    # used json to store the history in a json file in root directory as chat ended
    chat_history = cl.user_session.get("chat_history") or []
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f, indent=4)
