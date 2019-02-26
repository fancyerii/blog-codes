package com.fancyerii.blog.stanfordnlp.sentiment;

public class SentimentResult {
	String sentimentType;
	double sentimentScore;
	SentimentClassification sentimentClass;

	public String getSentimentType() {
		return sentimentType;
	}

	public void setSentimentType(String sentimentType) {
		this.sentimentType = sentimentType;
	}

	public double getSentimentScore() {
		return sentimentScore;
	}

	public void setSentimentScore(double sentimentScore) {
		this.sentimentScore = sentimentScore;
	}

	public SentimentClassification getSentimentClass() {
		return sentimentClass;
	}

	public void setSentimentClass(SentimentClassification sentimentClass) {
		this.sentimentClass = sentimentClass;
	}
}
