import os
import re
import nltk
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
#from langchain.prompts import PromptTemplate
import textstat
import subprocess


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize the OpenAI model
llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),  # Don't forget create your own .env
    model_name="gpt-3.5-turbo"
)

def words_to_tokens(word_count):
    """
    Converts word count to token count.
    """
    return int(word_count * 1.3)

def generate_seo_title(title, keyword):
    """
    Generates an SEO-friendly title based on the given title and primary keyword.
    """
    prompt = f"Create an SEO-friendly title for an article titled '{title}' with the primary keyword '{keyword}'."

    messages = [
        {"role": "system", "content": "You are an expert in SEO content creation. Your task is to generate SEO-friendly titles that incorporate the given keywords effectively."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = llm.invoke(messages)
        seo_title = response.content.strip()
        return seo_title
    except Exception as e:
        logging.error(f"An error occurred while generating the SEO title: {e}")
        return None

def generate_meta_description(title, keyword):
    """
    Generates a meta description for the article.
    """
    prompt = f"Write an engaging meta description for an article titled '{title}', focusing on '{keyword}'."

    messages = [
        {"role": "system", "content": "You are an expert in SEO content creation. Your task is to generate compelling meta descriptions that effectively incorporate the given keywords."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = llm.invoke(messages)
        meta_description = response.content.strip()
        return meta_description
    except Exception as e:
        logging.error(f"An error occurred while generating the meta description: {e}")
        return None

def generate_outline(title, keyword, secondary_keywords):
    """
    Generates the structure of the article.
    """
    secondary = ', '.join(secondary_keywords) if secondary_keywords else 'None'
    prompt = f"Create a detailed outline for an article titled '{title}', with the primary keyword '{keyword}' and secondary keywords '{secondary}'."

    messages = [
        {"role": "system", "content": "You are an expert in SEO content creation. Your task is to generate detailed and well-structured outlines for articles based on the given keywords."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = llm.invoke(messages)
        outline = response.content.strip()
        return outline
    except Exception as e:
        logging.error(f"An error occurred while generating the outline: {e}")
        return None

def generate_article(title, keyword, secondary_keywords, tone, length):
    """
    Generates an SEO-optimized article based on the given parameters.
    """
    length_mapping = {'short': 500, 'medium': 1000, 'long': 2000}
    word_count = length_mapping.get(length, 1000)
    max_tokens = words_to_tokens(word_count)
    max_allowed_tokens = 3000
    max_tokens = min(max_tokens, max_allowed_tokens)
    secondary = ', '.join(secondary_keywords) if secondary_keywords else 'None'
    prompt = (
        f"Write a {tone} article titled '{title}', focusing on the primary keyword '{keyword}' "
        f"and including secondary keywords '{secondary}'. The article should be approximately {word_count} words, "
        f"well-structured with appropriate headings and subheadings, and maintain a keyword density of around 1-2%. "
        f"Ensure the content is original, engaging, and easy to read. Use short sentences (average 15 words or fewer) and simple, everyday language to enhance readability. "
        f"Naturally incorporate the primary keyword '{keyword}' throughout the article to achieve the desired keyword density. "
        f"Do not exceed the specified word count."
    )

    messages = [
        {"role": "system", "content": "You are an expert in SEO content creation. Your task is to generate SEO-friendly articles that incorporate the given keywords effectively. Ensure that the content is easy to read and understand."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = llm.invoke(messages)
        article = response.content.strip()
        return article
    except Exception as e:
        logging.error(f"An error occurred while generating the article: {e}")
        return None

def evaluate_readability(article):
    """
    Evaluates the readability of the article using Flesch Reading Ease and Flesch-Kincaid Grade Level indexes.
    """
    flesch_score = textstat.flesch_reading_ease(article)
    fk_grade = textstat.flesch_kincaid_grade(article)
    return flesch_score, fk_grade

def evaluate_content_quality(article):
    """
    Uses the OpenAI model to assess the quality of the article's content.
    """
    prompt = f"Please evaluate the following article in terms of coherence, tone consistency, and overall quality:\n\n{article}\n\nEvaluation:"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = llm.invoke(messages)
        evaluation = response.content.strip()
        return evaluation
    except Exception as e:
        logging.error(f"An error occurred while evaluating the content: {e}")
        return None


def save_article_to_file(seo_title, meta_description, outline, article, flesch_score, fk_grade, content_evaluation,
                         file_name="generated_article_full.txt"):
    """
    Saves the generated article along with SEO title, meta description, outline, readability, and content evaluation to a .txt file.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("--- SEO Title ---\n")
            file.write(f"{seo_title}\n\n")

            file.write("--- Meta Description ---\n")
            file.write(f"{meta_description}\n\n")

            file.write("--- Article Outline ---\n")
            file.write(f"{outline}\n\n")

            file.write("--- Generated Article ---\n")
            file.write(f"{article}\n\n")

            file.write("--- Article Quality Assessment ---\n")
            if flesch_score and fk_grade:
                file.write(f"Flesch Reading Ease Score: {flesch_score:.2f}\n")
                file.write(f"Flesch-Kincaid Grade Level: {fk_grade:.2f}\n")
            else:
                file.write("Unable to calculate readability scores.\n")

            file.write("\n--- Content Evaluation ---\n")
            file.write(f"{content_evaluation}\n")

        logging.info(f"Article and its details successfully saved to {file_name}")
    except Exception as e:
        logging.error(f"An error occurred while saving the article and its details: {e}")

def main():
    """
    Main function to run the article generator and quality assessment.
    """
    try:
        # Collect user inputs
        title = input("Enter the article title: ").strip()
        keyword = input("Enter the primary keyword: ").strip()
        secondary_keywords_input = input("Enter secondary keywords (comma-separated, optional): ").strip()
        tone = input("Enter the desired tone (e.g., formal, informal, professional): ").strip()
        length = input("Enter the article length (short, medium, long): ").strip().lower()

        if not title or not keyword or not tone or not length:
            logging.warning("Title, primary keyword, tone, and length are required fields.")
            return

        secondary_keywords = [kw.strip() for kw in secondary_keywords_input.split(',')] if secondary_keywords_input else []

        # Generate SEO title and meta description
        logging.info("Generating SEO title and meta description...")
        seo_title = generate_seo_title(title, keyword)
        meta_description = generate_meta_description(title, keyword)

        # Generate article outline
        logging.info("Generating article outline...")
        outline = generate_outline(title, keyword, secondary_keywords)

        # Generate article
        logging.info("Generating article. Please wait, this may take a few minutes...")
        article = generate_article(title, keyword, secondary_keywords, tone, length)

        if not article:
            logging.error("Failed to generate the article.")
            return


        # Evaluate the article
        logging.info("Evaluating article quality...")
        flesch_score, fk_grade = evaluate_readability(article)
        content_evaluation = evaluate_content_quality(article)

        save_article_to_file(
            seo_title,
            meta_description,
            outline,
            article,
            flesch_score,
            fk_grade,
            content_evaluation
        )

        # Display results
        print("\n--- SEO Title ---\n")
        print(seo_title)
        print("\n--- Meta Description ---\n")
        print(meta_description)
        print("\n--- Article Outline ---\n")
        print(outline)
        print("\n--- Generated Article ---\n")
        print(article)
        print("\n--- Article Quality Assessment ---\n")
        if flesch_score and fk_grade:
            print(f"Flesch Reading Ease Score: {flesch_score:.2f}")
            print(f"Flesch-Kincaid Grade Level: {fk_grade:.2f}")
        else:
            print("Unable to calculate readability scores.")
        print("\n--- Content Evaluation ---\n")
        print(content_evaluation)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)


    with open('requirements.txt', 'wb') as f:
        f.write(result.stdout)

if __name__ == "__main__":
    main()
