package com.fancyerii.blog.stanfordnlp;

import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;

import java.util.*;

public class PipelineDemo {

	public static void main(String[] args) {
		// set up pipeline properties
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit");
		
		// set up pipeline
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		
		// the following has examples for the new Core Wrapper API and the older
		// Annotation API
		// example using Core Wrappers (new API designed to make it easier to work with
		// NLP data)
		System.out.println("---");
		System.out.println("Accessing Tokens In A CoreDocument");
		System.out.println("(text, char offset begin, char offset end)");
		CoreDocument exampleDocument = new CoreDocument("Here is the text to tokenize.");
		// annotate document
		pipeline.annotate(exampleDocument);
		// access tokens from a CoreDocument
		// a token is represented by a CoreLabel
		List<CoreLabel> firstSentenceTokens = exampleDocument.sentences().get(0).tokens();
		// this for loop will print out all of the tokens and the character offset info
		for (CoreLabel token : firstSentenceTokens) {
			System.out.println(token.word() + "\t" + token.beginPosition() + "\t" + token.endPosition());
		}
		// example using older Annotation API
		System.out.println("---");
		System.out.println("Accessing Tokens In An Annotation");
		System.out.println("(text, char offset begin, char offset end)");
		Annotation exampleAnnotation = new Annotation("Here is the text to tokenize.");
		pipeline.annotate(exampleAnnotation);
		CoreMap firstSentence = exampleAnnotation.get(CoreAnnotations.SentencesAnnotation.class).get(0);
		// this for loop will print out all of the tokens and the character offset info
		for (CoreLabel token : firstSentence.get(CoreAnnotations.TokensAnnotation.class)) {
			System.out.println(token.word() + "\t" + token.beginPosition() + "\t" + token.endPosition());
		}
	}
}