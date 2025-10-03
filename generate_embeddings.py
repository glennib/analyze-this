#!/usr/bin/env python3

"""
Embedding Generation Module

Generates embeddings from text using Google's Gemini API.
Can be used both from command line and imported programmatically.

Usage:
    CLI: ./generate_embeddings.py <input_file> <output_file>
    Python:
        from generate_embeddings import generate_embedding, save_embedding, load_embedding
        embedding = generate_embedding("some text")
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


# Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'models/text-embedding-004')


def generate_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
    """
    Generate embedding vector from text using Gemini API.

    Args:
        text: The text to embed
        task_type: The task type for the embedding. Options:
            - RETRIEVAL_DOCUMENT: For embeddings stored in a database for search
            - RETRIEVAL_QUERY: For embeddings of search queries
            - SEMANTIC_SIMILARITY: For measuring similarity between texts
            - CLASSIFICATION: For text classification
            - CLUSTERING: For clustering texts

    Returns:
        List of floats representing the embedding vector

    Raises:
        ValueError: If GEMINI_API_KEY is not set
        Exception: If API call fails
    """
    if not GEMINI_API_KEY:
        raise ValueError('GEMINI_API_KEY environment variable not set')

    # Gemini Embedding API URL
    api_url = f'https://generativelanguage.googleapis.com/v1beta/{EMBEDDING_MODEL}:embedContent?key={GEMINI_API_KEY}'

    request_data = {
        'model': EMBEDDING_MODEL,
        'content': {
            'parts': [{
                'text': text
            }]
        },
        'taskType': task_type
    }

    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(request_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

            if 'embedding' in data and 'values' in data['embedding']:
                return data['embedding']['values']
            else:
                raise Exception(f'Unexpected API response format: {data}')

    except urllib.error.HTTPError as e:
        error_text = e.read().decode('utf-8')
        raise Exception(f'Embedding API error: HTTP {e.code} - {error_text}')
    except Exception as e:
        raise Exception(f'Failed to generate embedding: {str(e)}')


def save_embedding(
    embedding: List[float],
    output_path: str,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Save embedding vector to JSON file with metadata.

    Args:
        embedding: The embedding vector to save
        output_path: Path where to save the embedding JSON file
        metadata: Optional metadata to include (source file, text preview, etc.)
    """
    output_data = {
        'embedding': embedding,
        'dimension': len(embedding),
        'model': EMBEDDING_MODEL,
        'metadata': metadata or {}
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)


def load_embedding(input_path: str) -> Tuple[List[float], Dict[str, Any]]:
    """
    Load embedding vector and metadata from JSON file.

    Args:
        input_path: Path to the embedding JSON file

    Returns:
        Tuple of (embedding_vector, metadata_dict)
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    embedding = data.get('embedding', [])
    metadata = data.get('metadata', {})

    return embedding, metadata


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embedding vectors.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Cosine similarity score between -1 and 1
    """
    if len(embedding1) != len(embedding2):
        raise ValueError('Embeddings must have same dimension')

    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
    magnitude1 = sum(a * a for a in embedding1) ** 0.5
    magnitude2 = sum(b * b for b in embedding2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def embed_file(
    input_path: str,
    output_path: str,
    task_type: str = "RETRIEVAL_DOCUMENT"
) -> None:
    """
    Generate embedding from text file and save to JSON.

    Args:
        input_path: Path to input text file
        output_path: Path to output JSON file
        task_type: Task type for embedding generation
    """
    # Read input text
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f'Input file not found: {input_path}')

    text = input_file.read_text(encoding='utf-8')

    # Generate embedding
    print(f'Generating embedding for {input_path}...', file=sys.stderr)
    embedding = generate_embedding(text, task_type=task_type)

    # Prepare metadata
    metadata = {
        'source_file': str(input_file),
        'text_length': len(text),
        'text_preview': text[:200] + ('...' if len(text) > 200 else '')
    }

    # Save embedding
    save_embedding(embedding, output_path, metadata)
    print(f'Saved embedding to {output_path}', file=sys.stderr)
    print(f'Embedding dimension: {len(embedding)}', file=sys.stderr)


def main():
    """CLI entry point"""
    if len(sys.argv) < 3:
        print('Usage: ./generate_embeddings.py <input_file> <output_file> [task_type]', file=sys.stderr)
        print('', file=sys.stderr)
        print('Task types:', file=sys.stderr)
        print('  RETRIEVAL_DOCUMENT (default) - For embeddings stored in a database', file=sys.stderr)
        print('  RETRIEVAL_QUERY - For search queries', file=sys.stderr)
        print('  SEMANTIC_SIMILARITY - For similarity comparison', file=sys.stderr)
        print('  CLASSIFICATION - For text classification', file=sys.stderr)
        print('  CLUSTERING - For clustering texts', file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    task_type = sys.argv[3] if len(sys.argv) > 3 else "RETRIEVAL_DOCUMENT"

    try:
        embed_file(input_path, output_path, task_type)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
