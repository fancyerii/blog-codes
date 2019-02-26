package com.fancyerii.blog.stanfordnlp;

import java.io.InputStream;
import java.io.StringReader;
import java.util.List;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.SentenceUtils;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger; 

public class TaggerDemo {

	private TaggerDemo() {
	}

	public static void main(String[] args) throws Exception { 
		InputStream input = TaggerDemo.class.getResourceAsStream("/"+MaxentTagger.DEFAULT_JAR_PATH);
 
		MaxentTagger tagger = new MaxentTagger(input);
		
		List<List<HasWord>> sentences = MaxentTagger.tokenizeText(new StringReader("Karma of humans is AI"));

		for (List<HasWord> sentence : sentences) {

			List<TaggedWord> tSentence = tagger.tagSentence(sentence);

			System.out.println(SentenceUtils.listToString(tSentence, false));

		}

	}

}
