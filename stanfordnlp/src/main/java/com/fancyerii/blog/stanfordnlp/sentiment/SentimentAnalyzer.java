package com.fancyerii.blog.stanfordnlp.sentiment;

import java.util.Properties;

import org.ejml.simple.SimpleMatrix;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;

public class SentimentAnalyzer {

	StanfordCoreNLP pipeline;

	public void initialize() {
		Properties properties = new Properties();
		properties.setProperty("annotators", "tokenize, ssplit, parse, sentiment");
		pipeline = new StanfordCoreNLP(properties);
	}

	public SentimentResult getSentimentResult(String text) {
		SentimentClassification classification = new SentimentClassification();
		SentimentResult sentimentResult = new SentimentResult();
		if (text != null && text.length() > 0) {
			Annotation annotation = pipeline.process(text);
			for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
				Tree tree = sentence.get(SentimentCoreAnnotations.SentimentAnnotatedTree.class);
				SimpleMatrix simpleMatrix = RNNCoreAnnotations.getPredictions(tree);

				classification.setVeryNegative((double) Math.round(simpleMatrix.get(0) * 100d));
				classification.setNegative((double) Math.round(simpleMatrix.get(1) * 100d));
				classification.setNeutral((double) Math.round(simpleMatrix.get(2) * 100d));
				classification.setPositive((double) Math.round(simpleMatrix.get(3) * 100d));
				classification.setVeryPositive((double) Math.round(simpleMatrix.get(4) * 100d));

				String setimentType = sentence.get(SentimentCoreAnnotations.SentimentClass.class);
				sentimentResult.setSentimentType(setimentType);
				sentimentResult.setSentimentClass(classification);
				sentimentResult.setSentimentScore(RNNCoreAnnotations.getPredictedClass(tree));
			}
		}
		return sentimentResult;
	}
}
