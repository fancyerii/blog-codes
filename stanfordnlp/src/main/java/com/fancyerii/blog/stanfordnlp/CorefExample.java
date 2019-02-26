package com.fancyerii.blog.stanfordnlp;

import java.util.Properties;

import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.coref.data.Mention;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class CorefExample {
	public static void main(String[] args) throws Exception {
		Annotation document = new Annotation(
				"Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008.");
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,coref");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(document);
		System.out.println("---");
		System.out.println("coref chains");
		for (CorefChain cc : document.get(CorefCoreAnnotations.CorefChainAnnotation.class).values()) {
			System.out.println("\t" + cc);
		}
		for (CoreMap sentence : document.get(CoreAnnotations.SentencesAnnotation.class)) {
			System.out.println("---");
			System.out.println("mentions");
			for (Mention m : sentence.get(CorefCoreAnnotations.CorefMentionsAnnotation.class)) {
				System.out.println("\t" + m);
			}
		}
	}
}
