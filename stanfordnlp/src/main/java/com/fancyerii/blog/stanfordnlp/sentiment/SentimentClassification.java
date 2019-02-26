package com.fancyerii.blog.stanfordnlp.sentiment;

public class SentimentClassification {

	/*
	 * "Very negative" = 0 "Negative" = 1 "Neutral" = 2 "Positive" = 3
	 * "Very positive" = 4
	 */

	double veryPositive;
	double positive;
	double neutral;
	double negative;
	double veryNegative;

	public double getVeryPositive() {
		return veryPositive;
	}

	public void setVeryPositive(double veryPositive) {
		this.veryPositive = veryPositive;
	}

	public double getPositive() {
		return positive;
	}

	public void setPositive(double positive) {
		this.positive = positive;
	}

	public double getNeutral() {
		return neutral;
	}

	public void setNeutral(double neutral) {
		this.neutral = neutral;
	}

	public double getNegative() {
		return negative;
	}

	public void setNegative(double negative) {
		this.negative = negative;
	}

	public double getVeryNegative() {
		return veryNegative;
	}

	public void setVeryNegative(double veryNegative) {
		this.veryNegative = veryNegative;
	}

}
