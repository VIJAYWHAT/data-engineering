package com.example;

import java.util.ArrayList;
import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

class ProductInfo {

    private String productName;
    private String productCode;
    private String availability;

    public ProductInfo(String productName, String productCode, String availability) {
        this.productName = productName;
        this.productCode = productCode;
        this.availability = availability;
    }

    @Override
    public String toString() {
        return "Product Name: " + productName + ", Product Code: " + productCode + ", Availability: " + availability;
    }
}

public class ScrapeMulticraft {

    public static List<ProductInfo> fetchProducts(String url) {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver"); // Set path to ChromeDriver
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage");
        WebDriver driver = new ChromeDriver(options);
        List<ProductInfo> productList = new ArrayList<>();

        try {
            driver.get(url);
            Thread.sleep(5000); // Allow page to load fully
            Document doc = Jsoup.parse(driver.getPageSource());
            Elements productSections = doc.select("li.skuSummary");

            if (!productSections.isEmpty()) {
                for (Element entry : productSections) {
                    String productName = entry.select("div.skuSummary-desc").text();
                    String productCode = entry.select("p.summary-id").text();
                    String availability = entry.select("div.row p").size() > 1 ? entry.select("div.row p").get(1).text() : "N/A";
                    productList.add(new ProductInfo(productName, productCode, availability));
                }
            } else {
                System.out.println("Error: No products found on the page.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            driver.quit();
        }
        return productList;
    }

    public static void main(String[] args) {
        String url = "https://multicraft.ca/en/brand/subbrands?code=artscrafts";
        List<ProductInfo> productData = fetchProducts(url);

        if (!productData.isEmpty()) {
            int i = 1;
            for (ProductInfo product : productData) {
                System.out.println(i + " - " + product);
                i++;
            }
        } else {
            System.out.println("No product data found or website structure has changed.");
        }
    }
}
