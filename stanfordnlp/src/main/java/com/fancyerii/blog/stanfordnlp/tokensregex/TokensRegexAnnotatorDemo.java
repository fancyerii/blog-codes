package com.fancyerii.blog.stanfordnlp.tokensregex;

import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;
import java.util.List;
import java.util.Properties;

public class TokensRegexAnnotatorDemo {

	// key for matched expressions
	public static class MyMatchedExpressionAnnotation implements CoreAnnotation<List<CoreMap>> {
		@Override
		public Class<List<CoreMap>> getType() {
			return ErasureUtils.<Class<List<CoreMap>>>uncheckedCast(String.class);
		}
	}

	public static void main(String[] args) throws ClassNotFoundException {
		// set properties
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,tokensregex");
		props.setProperty("tokensregex.rules", "basic_ner.rules");
		props.setProperty("tokensregex.matchedExpressionsAnnotationKey",
				"com.fancyerii.blog.stanfordnlp.tokensregex.TokensRegexAnnotatorDemo$MyMatchedExpressionAnnotation");
		// build pipeline
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		// annotate
		Annotation ann = new Annotation("There will be a big announcement by Apple Inc today at 5:00pm.  "
				+ "She has worked at Miller Corp. for 5 years.");
		pipeline.annotate(ann);
		// show results
		System.out.println("---");
		System.out.println("tokens\n");
		for (CoreMap sentence : ann.get(CoreAnnotations.SentencesAnnotation.class)) {
			for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {
				System.out.println(token.word() + "\t" + token.ner());
			}
			System.out.println("");
		}
		System.out.println("---");
		System.out.println("matched expressions\n");
		for (CoreMap me : ann.get(MyMatchedExpressionAnnotation.class)) {
			System.out.println(me);
		}
	}
}
