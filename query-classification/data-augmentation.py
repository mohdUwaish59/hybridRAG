import pandas as pd
from transformers import pipeline
import time

def augment_questions(questions, model_name="t5-base", num_return_sequences=1, max_retries=3):
    """Paraphrase questions using a text generation model from Hugging Face."""
    try:
        paraphrase_pipeline = pipeline("text2text-generation", model=model_name, tokenizer=model_name)
    except Exception as e:
        print(f"❌ Error initializing model: {e}")
        return []
    
    augmented_questions = []
    print(f"Starting augmentation using model: {model_name}")
    
    for i, question in enumerate(questions):
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            try:
                result = paraphrase_pipeline(f"paraphrase: {question}", max_length=50, num_return_sequences=num_return_sequences)
                augmented_questions.append(result[0]['generated_text'])
                success = True  # Mark as successful
            except Exception as e:
                retry_count += 1
                print(f"⚠️ Error processing question {i} (Retry {retry_count}/{max_retries}): {e}")
                time.sleep(2)  # Small delay before retrying

        if not success:
            print(f"❌ Failed to process question {i} after {max_retries} retries. Using original question.")
            augmented_questions.append(question)  # Use original question to avoid data loss

        if i % 50 == 0:
            print(f"✅ Processed {i+1}/{len(questions)} questions...")
        time.sleep(1)  # Avoid overloading the model

    return augmented_questions

def save_augmented_dataset(original_df, augmented_questions, output_path):
    """Save the augmented dataset to a new file."""
    augmented_df = pd.DataFrame({
        "Questions": augmented_questions,
        "Query_Type": original_df['Query_Type'].iloc[:len(augmented_questions)].tolist(),
    })
    combined_df = pd.concat([original_df, augmented_df], ignore_index=True)
    combined_df.to_csv(output_path, index=False)
    print(f"✅ Augmented dataset saved to {output_path}")

if __name__ == "__main__":
    # Generate initial dataset of 5000 questions
    num_rows = 5000
    query_types = ["Explicit Fact", "Implicit Fact", "Interpretable Rationale", "Hidden Rationale"]
    base_questions = {
        "Explicit Fact": "What are the major elements in basalt rock?",
        "Implicit Fact": "How does CO2 influence pH in groundwater?",
        "Interpretable Rationale": "What geochemical models predict mineral dissolution?",
        "Hidden Rationale": "How do rare earth elements indicate crustal processes?"
    }
    
    data = []
    for i in range(num_rows):
        query_type = query_types[i % len(query_types)]
        data.append({
            "Questions": base_questions[query_type],
            "Query_Type": query_type
        })
    
    df = pd.DataFrame(data)
    print("✅ Original dataset loaded successfully.")

    # Generate augmented questions
    print("🔄 Generating augmented questions...")
    augmented_questions = augment_questions(df['Questions'], model_name="t5-base", num_return_sequences=1)
    print(f"✅ Generated {len(augmented_questions)} augmented questions.")

    # Save the augmented dataset
    output_file = "augmented_research_geochemistry_questions.csv"
    save_augmented_dataset(df, augmented_questions, output_file)
