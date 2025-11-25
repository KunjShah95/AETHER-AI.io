// Search utilities for documentation

export interface SearchableItem {
    id: string;
    section: string;
    sectionTitle: string;
    category?: string;
    title: string;
    description: string;
    content: string;
    keywords: string[];
}

export interface SearchResult {
    item: SearchableItem;
    score: number;
    matchedFields: string[];
    highlightedContent?: string;
}

/**
 * Normalize text for search comparison
 */
export function normalizeText(text: string): string {
    return text.toLowerCase().trim();
}

/**
 * Calculate relevance score for a search match
 */
export function calculateRelevanceScore(
    item: SearchableItem,
    query: string,
    matchedFields: string[]
): number {
    const normalizedQuery = normalizeText(query);
    let score = 0;

    // Title match is most important
    if (matchedFields.includes('title')) {
        const titleMatch = normalizeText(item.title).includes(normalizedQuery);
        if (titleMatch) {
            score += normalizeText(item.title).startsWith(normalizedQuery) ? 100 : 50;
        }
    }

    // Category match
    if (matchedFields.includes('category') && item.category) {
        score += 30;
    }

    // Description match
    if (matchedFields.includes('description')) {
        score += 20;
    }

    // Keywords match
    if (matchedFields.includes('keywords')) {
        const exactKeywordMatch = item.keywords.some(
            k => normalizeText(k) === normalizedQuery
        );
        score += exactKeywordMatch ? 40 : 15;
    }

    // Content match
    if (matchedFields.includes('content')) {
        score += 10;
    }

    // Section title match
    if (matchedFields.includes('sectionTitle')) {
        score += 25;
    }

    return score;
}

/**
 * Search through items and return ranked results
 */
export function searchItems(
    items: SearchableItem[],
    query: string
): SearchResult[] {
    if (!query || query.trim().length === 0) {
        return [];
    }

    const normalizedQuery = normalizeText(query);
    const results: SearchResult[] = [];

    for (const item of items) {
        const matchedFields: string[] = [];

        // Check each field for matches
        if (normalizeText(item.title).includes(normalizedQuery)) {
            matchedFields.push('title');
        }

        if (item.category && normalizeText(item.category).includes(normalizedQuery)) {
            matchedFields.push('category');
        }

        if (normalizeText(item.description).includes(normalizedQuery)) {
            matchedFields.push('description');
        }

        if (normalizeText(item.content).includes(normalizedQuery)) {
            matchedFields.push('content');
        }

        if (normalizeText(item.sectionTitle).includes(normalizedQuery)) {
            matchedFields.push('sectionTitle');
        }

        if (item.keywords.some(k => normalizeText(k).includes(normalizedQuery))) {
            matchedFields.push('keywords');
        }

        // If there are matches, add to results
        if (matchedFields.length > 0) {
            const score = calculateRelevanceScore(item, query, matchedFields);
            const highlightedContent = highlightMatch(item.description, query);

            results.push({
                item,
                score,
                matchedFields,
                highlightedContent
            });
        }
    }

    // Sort by relevance score (highest first)
    return results.sort((a, b) => b.score - a.score);
}

/**
 * Highlight matching text in content
 */
export function highlightMatch(text: string, query: string): string {
    if (!query || !text) return text;

    const normalizedQuery = normalizeText(query);
    const normalizedText = normalizeText(text);

    const index = normalizedText.indexOf(normalizedQuery);
    if (index === -1) return text;

    // Extract context around the match
    const contextLength = 100;
    const start = Math.max(0, index - contextLength / 2);
    const end = Math.min(text.length, index + normalizedQuery.length + contextLength / 2);

    let excerpt = text.substring(start, end);
    if (start > 0) excerpt = '...' + excerpt;
    if (end < text.length) excerpt = excerpt + '...';

    return excerpt;
}

/**
 * Get excerpt from content
 */
export function getExcerpt(text: string, maxLength: number = 150): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}
