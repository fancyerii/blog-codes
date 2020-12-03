package com.github.fancyerii.wechatdriver;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.time.Duration;
import java.util.Arrays;
import java.util.List;

import static org.openqa.selenium.support.ui.ExpectedConditions.presenceOfElementLocated;

public class WechatDriver {
    public static void main(String[] args) throws IOException {
        ChromeOptions options = new ChromeOptions();
        WebDriver driver=new ChromeDriver(options);
        System.setProperty("webdriver.chrome.driver", "/home/lili/soft/chromedriver");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(30).getSeconds());
        try {
            driver.get("http://wx.qq.com/");
            WebElement qrImg=wait.until(presenceOfElementLocated(By.xpath("//DIV[@class='qrcode']/IMG")));

            byte[] bytes=qrImg.getScreenshotAs(OutputType.BYTES);
            int tryCount=0;
            for(;tryCount<10;tryCount++){
                if(ImageTools.isQRCodeImage(bytes)){
                    break;
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                }
                bytes=qrImg.getScreenshotAs(OutputType.BYTES);
            }
            if(tryCount == 10){
                throw new RuntimeException("找不到二维码");
            }
            //TODO 把二维码发送给人扫描登录
            //这里只是把二维码保存下来，实际上二维码是有有效期的，需要定期刷新。
            File tmpFile=File.createTempFile("tmp-qr", ".png");
            Files.write(tmpFile.toPath(), bytes);
            System.out.println("请扫描 "+tmpFile.getAbsolutePath()+" 登录");

            //检查是否找不到二维码从而判断已经扫码
            while(true){
                qrImg=findElement(driver, By.xpath("//DIV[@class='qrcode']/IMG"));
                if(qrImg==null) break;
                byte[] newImg=qrImg.getScreenshotAs(OutputType.BYTES);
                if(!Arrays.equals(bytes, newImg)){
                    bytes=newImg;
                    Files.write(tmpFile.toPath(), bytes);
                }
                System.out.println("请扫描 "+tmpFile.getAbsolutePath()+" 登录");
                try {
                    Thread.sleep(10000);
                } catch (InterruptedException e) {
                }
            }
            //判断是否被禁用
            String body=findElement(driver,By.xpath("//BODY")).getAttribute("innerHTML");
            if(body.contains("为了你的帐号安全，此微信号已不允许登录网页微信。")){
                throw new RuntimeException("您的账号不能用网页版登录");
            }
            WebElement searchInput=wait.until(presenceOfElementLocated(By.xpath("//INPUT[@placeholder='搜索']")));
            searchInput.sendKeys("文件传输助手");
            WebElement searchResult=wait.until(presenceOfElementLocated(By.xpath("//DIV[@class='info']/H4[text()='文件传输助手']")));
            searchResult.click();
            WebElement editDiv=wait.until(presenceOfElementLocated(By.xpath("//PRE[@id='editArea']")));
            editDiv.sendKeys("明天有空吗？");

            WebElement sendButton=wait.until(presenceOfElementLocated(By.xpath("//A[@class='btn btn_send']")));
            sendButton.click();

        }finally {
            //TODO 退出登录
            //目前建议人工点击退出
            driver.quit();
        }
    }

    private static WebElement findElement(WebDriver driver, By by){
        try {
            return driver.findElement(by);
        }catch(Exception e){
            return null;
        }
    }

}
