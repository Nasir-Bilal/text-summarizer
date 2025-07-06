from transformers import pipeline, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(content, depth=0, max_depth=3):
    maxTokenLength = 1000
    tokensLength = len(tokenizer.encode(content, truncation=False))

    if tokensLength < maxTokenLength or depth >= max_depth:
        min_len = int(0.05 * tokensLength)
        max_len = int(0.15 * tokensLength)
        return summarizer_pipeline(content, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']

    # Break into chunks
    numChunks = (tokensLength // maxTokenLength) + 1
    chunkSize = len(content) // numChunks

    chunkSummaries = []
    for i in range(numChunks):
        chunk = content[i * chunkSize : (i + 1) * chunkSize]
        chunk_tokens = len(tokenizer.encode(chunk, truncation=False))
        min_len = int(0.05 * chunk_tokens)
        max_len = int(0.15 * chunk_tokens)
        summary = summarizer_pipeline(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
        chunkSummaries.append(summary)

    finalSummary = " ".join(chunkSummaries)
    return summarize_text(finalSummary, depth + 1, max_depth)
