![cover](https://media.discordapp.net/attachments/713817450130571416/1208728527323668520/cover.png?ex=65e4572a&is=65d1e22a&hm=7f169f9aa186d86b8814c0dd124c3486e2db7280886fdf56d9dbf43ac4643e20&=&format=webp&quality=lossless&width=1410&height=452)
# BlurredAI 
Hide your data from GPT-4 with local models on your laptop! 

## Inspiration

Have you ever had sensitive questions or data that you didn't feel comfortable sending to ChatGPT? Probably all the time for your corporate activity—work emails, legal texts, internal finances. This extends beyond corporate use cases though; think about your medical history, tax forms, relationship problems. This is a clear gap: **remote models are already sufficiently powerful for most tasks, but they're untrustworthy to deal with confidential information and hosting similarly powerful models locally can be expensive.**

## What it does

Our project, BlurredAI, enables a collaboration between small & large models. A lightweight LLM, hosted locally on your laptop, privatizes your queries on private data before sending them to powerful remote models such as GPT-4. It then reconstructs the original context/data locally from the remote response, ensuring privacy without compromising the quality of insights. Check our demo video for concrete examples!

## How we built it

There are a few core components to BlurredAI:
1. Hosting large language models locally, essential for privacy guarantees.
2. Adapting local models to different workflows, such as privatizing emails, parsing legal texts, understanding spreadsheets.
3. A natural, intuitive UI where users can chat with and ask questions about their sensitive texts, documents, or PDFs.

For #1 we used TogetherAI for local development and (plan to use) Ollama for hosting on laptops. For #2, we crafted numerous prompts for different privacy workflows. For #3, we employed Streamlit for the frontend and Python, including PDF & CSV parsers, for the backend.

## Challenges we ran into


- Local models often aren't powerful enough to coherently privatize sensitive data, presenting an efficiency-utility trade-off.
- Adapting the local models to various workflows; for example, the work done by the local model varies greatly between making spreadsheets private and making legal texts private.


## Accomplishments that we're proud of

The novelty of our idea is what sets us apart. Unlike other companies, we are not taking the user's data. We don't even have a database. The user (business/individual) needs to simply clone our open-source repository and run the app locally.


## What we learned


- Privacy is multi-faceted and context-dependent. In some cases, it means redacting names, numbers, and emails, while in others it involves providing plausible deniability to the user.
- Open-source LLMs for local hosting are still brittle, lacking strong reasoning capabilities without specific adaptations for different workflows.
- Beyond standard privacy/cryptography tools, user-acceptable private inference can be achieved through a combination of appropriate anonymization, distributed computing, and careful human-computer interface design.




## What's next for BlurredAI

- Publishing as a PyPi package to simplify installation.
- Extending to early adopters (e.g., mid-size companies like Esri) based on our user research.
- Enhancing the local model for privatization (e.g., text redaction, rephrasing, shifting points of view) through better prompts, local fine-tuning, or integrating larger open-source models locally.





