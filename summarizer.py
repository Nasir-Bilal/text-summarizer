from transformers import pipeline, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(content, compression_ratio=30, depth=0, max_depth=10):
    maxTokenLength = 1000
    tokensLength = len(tokenizer.encode(content, truncation=False))

    if tokensLength < maxTokenLength or depth >= max_depth:
        min_len = max(20, int((compression_ratio / 100) * tokensLength * 0.5))
        max_len = max(40, int((compression_ratio / 100) * tokensLength))
        return summarizer_pipeline(content, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']

    # Break into chunks
    numChunks = (tokensLength // maxTokenLength) + 1
    chunkSize = len(content) // numChunks

    chunkSummaries = []
    for i in range(numChunks):
        chunk = content[i * chunkSize : (i + 1) * chunkSize]
        chunk_tokens = len(tokenizer.encode(chunk, truncation=False))
        min_len_chunk = max(20, int((compression_ratio / 100) * chunk_tokens * 0.5))
        max_len_chunk = max(40, int((compression_ratio / 100) * chunk_tokens))
        
        summary = summarizer_pipeline(
            chunk,
            max_length=max_len_chunk,
            min_length=min_len_chunk,
            do_sample=False
        )[0]['summary_text']

        chunkSummaries.append(summary)

    finalSummary = " ".join(chunkSummaries)
    return summarize_text(
        finalSummary,
        compression_ratio=compression_ratio,
        depth=depth + 1,
        max_depth=max_depth
    )
