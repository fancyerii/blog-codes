package com.fancyerii.blog.stanfordnlp.sentiment;


public class SentimentAnalysis {

	public static void main(String[] args) {

		// String text = "A year spent in artificial intelligence is enough to make one
		// believe in God." +
		// "There is no reason and no way that a human mind can keep up with an
		// artificial intelligence machine by 2035." +
		// "Is artificial intelligence less than our intelligence?";
		String text = "Never underestimate yourself you are much more than you think\n" + "";
		SentimentAnalyzer sentimentAnalyzer = new SentimentAnalyzer();
		sentimentAnalyzer.initialize();
		SentimentResult sentimentResult = sentimentAnalyzer.getSentimentResult(text);

		System.out.println("Very positive: " + sentimentResult.getSentimentClass().getVeryPositive() + "%");
		System.out.println("Positive: " + sentimentResult.getSentimentClass().getPositive() + "%");
		System.out.println("Neutral: " + sentimentResult.getSentimentClass().getNeutral() + "%");
		System.out.println("Negative: " + sentimentResult.getSentimentClass().getNegative() + "%");
		System.out.println("Very negative: " + sentimentResult.getSentimentClass().getVeryNegative() + "%");
		System.out.println("Sentiment Score: " + sentimentResult.getSentimentScore());
		System.out.println("Sentiment Type: " + sentimentResult.getSentimentType());

	}

}
