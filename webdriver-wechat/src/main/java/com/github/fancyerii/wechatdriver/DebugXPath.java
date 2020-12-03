package com.github.fancyerii.wechatdriver;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

public class DebugXPath {
    public static void main(String[] args) throws IOException {
        ChromeOptions options = new ChromeOptions();
        WebDriver driver=new ChromeDriver(options);
        System.setProperty("webdriver.chrome.driver", "/home/lili/soft/chromedriver");
        debug(driver);
    }


    private static void debug(WebDriver driver) throws IOException {
        BufferedReader br=new BufferedReader(new InputStreamReader(System.in,"UTF-8"));
        String line;
        while((line=br.readLine())!=null){
            if(line.equals("quit")) break;
            if(line.startsWith("eval:")){
                String xpath=line.substring("eval:".length());
                System.out.println("eval xpath: "+xpath);
                try {
                    List<WebElement> elems = driver.findElements(By.xpath(xpath));
                    System.out.println("found: "+elems.size());
                    for(WebElement elem:elems){
                        String outerHtml=elem.getAttribute("outerHTML");
                        if(outerHtml.length()>10000){
                            outerHtml=outerHtml.substring(0, 10000)+"...";
                        }
                        System.out.println("****"+elem.getTagName()+", "+elem.getText()+", "+outerHtml);
                    }
                }catch(Exception e){
                    e.printStackTrace();
                }
            }else if(line.startsWith("click:")){
                String xpath=line.substring("click:".length());
                System.out.println("click xpath: "+xpath);
                try{
                    WebElement elem=driver.findElement(By.xpath(xpath));
                    elem.click();
                }catch(Exception e){
                    e.printStackTrace();
                }
            }else if(line.startsWith("sendtxt:")){
                String s=line.substring("sendtxt:".length());
                String[] arr=s.split("###");
                System.out.println("xpath: "+arr[0]+", send text: "+arr[1]);
                try{
                    WebElement elem=driver.findElement(By.xpath(arr[0]));
                    elem.sendKeys(arr[1]);
                }catch(Exception e){
                    e.printStackTrace();
                }
            }else{
                System.out.println("未知命令!!! 目前仅支持：\n1. eval:XPATH-->查看xpath\n2. click:XPATH-->点击XPATH的元素\n" +
                        "3.sendtxt:XPATH###TEXT-->给XPATH的元素发送文本TEXT\n如果想退出请输入quit");
            }

        }

        br.close();
    }
}
