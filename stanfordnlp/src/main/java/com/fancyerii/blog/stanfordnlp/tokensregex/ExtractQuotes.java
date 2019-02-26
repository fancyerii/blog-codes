package com.fancyerii.blog.stanfordnlp.tokensregex;

import org.apache.commons.io.IOUtils;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ling.tokensregex.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;
 
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Properties;
import java.util.regex.*;

public class ExtractQuotes {
 
	public static void main(String[] args) throws Exception{
		
		// get the text to process

		// load sentences
		String exampleSentences = IOUtils.toString(ExtractQuotes.class.getResourceAsStream("/basic_quote_extraction.txt"),
				StandardCharsets.UTF_8);

		// build pipeline to get sentences and do basic tagging
		Properties pipelineProps = new Properties();
		pipelineProps.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner");
		pipelineProps.setProperty("ner.applyFineGrained", "false");
		pipelineProps.setProperty("ssplit.eolonly", "true");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(pipelineProps);

		// get sentences
		Annotation exampleSentencesAnnotation = new Annotation(exampleSentences);
		pipeline.annotate(exampleSentencesAnnotation);

		// set up the TokensRegex pipeline

		// get the rules files
		//String[] rulesFiles = props.getProperty("rulesFiles").split(",");
		String ruleStr=IOUtils.toString(ExtractQuotes.class.getResourceAsStream("/basic_quote_extraction.rules"),
				StandardCharsets.UTF_8);
		
		// set up an environment with reasonable defaults
		Env env = TokenSequencePattern.getNewEnv();
		// set to case insensitive
		env.setDefaultStringMatchFlags(NodePattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);
		env.setDefaultStringPatternFlags(Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);

		// build the CoreMapExpressionExtractor
		
		CoreMapExpressionExtractor extractor = CoreMapExpressionExtractor.createExtractorFromString(env, ruleStr);

		// for each sentence in the input text, run the TokensRegex pipeline
		int sentNum = 0;
		for (CoreMap sentence : exampleSentencesAnnotation.get(CoreAnnotations.SentencesAnnotation.class)) {
			System.out.println("---");
			System.out.println("sentence number: " + sentNum);
			System.out.println("sentence text: " + sentence.get(CoreAnnotations.TextAnnotation.class));
			sentNum++;
			List<MatchedExpression> matchedExpressions = extractor.extractExpressions(sentence);
			// print out the results of the rules actions
			for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {
				System.out.println(token.word() + "\t" + token.tag() + "\t" + token.ner());
			}
			// print out the matched expressions
			for (MatchedExpression me : matchedExpressions) {
				System.out.println("matched expression: " + me.getText());
				System.out.println("matched expression value: " + me.getValue());
				System.out.println("matched expression char offsets: " + me.getCharOffsets());
				System.out.println(
						"matched expression tokens:" + me.getAnnotation().get(CoreAnnotations.TokensAnnotation.class));
			}
		}
	}

}
