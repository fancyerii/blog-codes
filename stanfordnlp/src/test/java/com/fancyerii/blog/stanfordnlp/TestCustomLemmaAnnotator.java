package com.fancyerii.blog.stanfordnlp;

import java.util.List;
import java.util.Properties;

import org.junit.Test;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;

public class TestCustomLemmaAnnotator {
	@Test
	public void test() {
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,custom.lemma");
		props.setProperty("customAnnotatorClass.custom.lemma", "com.fancyerii.blog.stanfordnlp.CustomLemmaAnnotator");
		props.setProperty("custom.lemma.lemmaFile", "custom-lemmas.txt");
		// set up pipeline
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		
		CoreDocument exampleDocument = new CoreDocument("Some many goods there.");
		// annotate document
		pipeline.annotate(exampleDocument);
		// access tokens from a CoreDocument
		// a token is represented by a CoreLabel
		List<CoreLabel> firstSentenceTokens = exampleDocument.sentences().get(0).tokens();
		// this for loop will print out all of the tokens and the character offset info
		for (CoreLabel token : firstSentenceTokens) {
			System.out.println(token.word()+"/"+token.getString(LemmaAnnotation.class) + "\t" + token.beginPosition() + "\t" + token.endPosition());
		}
	}
}
