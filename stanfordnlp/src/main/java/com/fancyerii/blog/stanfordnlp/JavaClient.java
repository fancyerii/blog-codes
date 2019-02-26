package com.fancyerii.blog.stanfordnlp;

import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.MultiLangsStanfordCoreNLPClient;
import edu.stanford.nlp.util.CoreMap;

public class JavaClient {
	public static void main(String[] args) {
		// creates a StanfordCoreNLP object with POS tagging, lemmatization, NER, parsing, and coreference resolution
		Properties props = new Properties();
		
		props.setProperty("annotators", "tokenize,ssplit,pos,ner,depparse,openie"); 
		MultiLangsStanfordCoreNLPClient pipeline = new MultiLangsStanfordCoreNLPClient(props, "http://localhost", 9000, 2, null, null, "zh");
 
		// read some text in the text variable
		String text = "今天天气很好。";
		// create an empty Annotation just with the given text
		Annotation document = new Annotation(text);
		// run all Annotators on this text
		pipeline.annotate(document);
		
		CoreMap firstSentence = document.get(CoreAnnotations.SentencesAnnotation.class).get(0);
		// this for loop will print out all of the tokens and the character offset info
		for (CoreLabel token : firstSentence.get(CoreAnnotations.TokensAnnotation.class)) {
			System.out.println(token.word() + "\t" + token.beginPosition() + "\t" + token.endPosition());
		}
	}
}
